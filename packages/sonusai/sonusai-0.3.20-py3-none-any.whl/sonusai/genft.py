"""genft

usage: genft [-hvs] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database JSON file.
    -i MIXID, --mixid MIXID         Mixture IDs JSON file.
    -o OUTPUT, --output OUTPUT      Output HDF5 file.
    -s, --segsnr                    Save segsnr. [default: False].

Generate a SonusAI feature/truth file from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database JSON file.
    MIXID       A JSON file containing a list of mixture IDs. The list should be named 'mixid'.
                If no file is provided, then all mixtures in the database will be generated.

Outputs:
    OUTPUT.h5   A SonusAI feature HDF5 file. Contains:
                    dataset:    feature
                    dataset:    truth_f
                    dataset:    segsnr (optional)
                    attribute:  mixdb
    genft.log

"""

import ctypes
import json
import multiprocessing
import time
from os.path import splitext
from typing import List
from typing import Union

import h5py
import numpy as np
from docopt import docopt
from pyaaware import FeatureGenerator
from pyaaware import ForwardTransform
from tqdm import tqdm

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import apply_augmentation
from sonusai.mixture import audio_files_exist
from sonusai.mixture import build_noise_audio_db
from sonusai.mixture import build_target_audio_db
from sonusai.mixture import get_audio_and_truth_t
from sonusai.mixture import get_total_class_count
from sonusai.mixture import load_mixdb
from sonusai.mixture import load_mixid
from sonusai.mixture import new_mixdb_from_mixid
from sonusai.mixture import set_mixture_offsets
from sonusai.mixture import truth_reduction
from sonusai.utils import grouper
from sonusai.utils import human_readable_size
from sonusai.utils import int16_to_float
from sonusai.utils import p_map
from sonusai.utils import seconds_to_hms
from sonusai.utils import to_numpy_array
from sonusai.utils import trim_docstring

genft_global = dict()


# noinspection PyGlobalUndefined

def mp_init(mixture_: multiprocessing.Array,
            truth_t_: multiprocessing.Array,
            segsnr_: multiprocessing.Array) -> None:
    global mp_mixture
    global mp_truth_t
    global mp_segsnr

    mp_mixture = mixture_
    mp_truth_t = truth_t_
    mp_segsnr = segsnr_


def init(mixdb: dict,
         mixid: Union[str, List[int]],
         start_offset: int = 0,
         logging: bool = True) -> (dict, int, int, int):
    mixdb_out = new_mixdb_from_mixid(mixdb=mixdb, mixid=mixid)

    total_samples = sum([sub['samples'] for sub in mixdb_out['mixtures']])
    transform_frames = total_samples // mixdb_out['frame_size']
    feature_frames = total_samples // mixdb_out['feature_step_samples'] - start_offset

    if logging:
        logger.info('')
        logger.info(f'Found {len(mixdb_out["mixtures"])} mixtures to process')
        logger.info(f'{total_samples} samples, {transform_frames} transform frames, {feature_frames} feature frames')

    return mixdb_out, total_samples, transform_frames, feature_frames


def genft(mixdb: dict,
          mixid: Union[str, List[int]],
          start_offset: int = 0,
          compute_segsnr: bool = False,
          logging: bool = True,
          show_progress: bool = False,
          progress: tqdm = None,
          parallel: bool = True) -> (np.ndarray, np.ndarray, dict):
    mixdb_out, total_samples, transform_frames, feature_frames = init(mixdb=mixdb,
                                                                      mixid=mixid,
                                                                      start_offset=start_offset,
                                                                      logging=logging)

    genft_global['mixdb'] = mixdb_out
    genft_global['total_samples'] = total_samples
    genft_global['transform_frames'] = transform_frames
    genft_global['compute_segsnr'] = compute_segsnr
    genft_global['noise_audios'] = build_noise_audio_db(mixdb_out)
    genft_global['target_audios'] = build_target_audio_db(mixdb_out)

    fft = ForwardTransform(N=mixdb_out['frame_size'] * 4, R=mixdb_out['frame_size'])
    mp_mixture = multiprocessing.Array(ctypes.c_float, transform_frames * fft.bins * 2)
    mp_truth_t = multiprocessing.Array(ctypes.c_float, total_samples * mixdb_out['num_classes'])
    mp_segsnr = multiprocessing.Array(ctypes.c_float, 0)
    if compute_segsnr:
        mp_segsnr = multiprocessing.Array(ctypes.c_float, transform_frames)

    mixture = to_numpy_array(mp_mixture, dtype=np.csingle).reshape((transform_frames, fft.bins))
    truth_t = to_numpy_array(mp_truth_t, dtype=np.single).reshape((total_samples, mixdb_out['num_classes']))
    segsnr = np.empty(0, dtype=np.single)
    if compute_segsnr:
        segsnr = to_numpy_array(mp_segsnr, dtype=np.single)

    fg = FeatureGenerator(frame_size=mixdb_out['frame_size'],
                          feature_mode=mixdb_out['feature'],
                          num_classes=mixdb_out['num_classes'],
                          truth_mutex=mixdb_out['truth_mutex'])

    feature = np.empty((feature_frames, fg.stride, fg.num_bands), dtype=np.single)
    truth_f = np.empty((feature_frames, fg.num_classes), dtype=np.single)

    # First pass to get offsets
    set_mixture_offsets(mixdb_out)

    # Second pass to get mixture and truth_t
    progress_needs_close = False
    if progress is None:
        progress = tqdm(total=len(mixdb_out['mixtures']), desc='genft', disable=not show_progress)
        progress_needs_close = True

    if parallel:
        p_map(process_mixture, mixdb_out['mixtures'], progress=progress, initializer=mp_init, initargs=(mp_mixture,
                                                                                                        mp_truth_t,
                                                                                                        mp_segsnr))
    else:
        mp_init(mp_mixture, mp_truth_t, mp_segsnr)
        for record in mixdb_out['mixtures']:
            process_mixture(record)
            progress.update()

    # Third pass to get features and truth_f
    feature_frame = 0
    for transform_frame in range(transform_frames):
        indices = slice(transform_frame * mixdb_out['frame_size'], (transform_frame + 1) * mixdb_out['frame_size'])
        fg.execute(mixture[transform_frame], truth_reduction(truth_t[indices], mixdb_out['truth_reduction_function']))

        if fg.eof():
            # start_offset is used when generating one batch at a time and makes it
            # possible to preserve the mixture data sequence across batch boundaries
            if start_offset != 0:
                start_offset -= 1
            else:
                feature[feature_frame] = fg.feature()
                truth_f[feature_frame] = fg.truth()
                feature_frame += 1

    if progress_needs_close:
        progress.close()

    mixdb_out['class_count'] = get_total_class_count(mixdb_out)

    duration = total_samples / sonusai.mixture.sample_rate
    if logging:
        logger.info('')
        logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
        logger.info(f'feature:  {human_readable_size(feature.nbytes, 1)}')
        logger.info(f'truth_f:  {human_readable_size(truth_f.nbytes, 1)}')
        if compute_segsnr:
            logger.info(f'segsnr:   {human_readable_size(segsnr.nbytes, 1)}')

    return feature, truth_f, segsnr, mixdb_out


def process_mixture(record: dict) -> None:
    fft = ForwardTransform(N=genft_global['mixdb']['frame_size'] * 4, R=genft_global['mixdb']['frame_size'])

    mixture = to_numpy_array(mp_mixture, dtype=np.csingle).reshape((genft_global['transform_frames'], fft.bins))
    truth_t = to_numpy_array(mp_truth_t, dtype=np.single)
    truth_t = truth_t.reshape((genft_global['total_samples'], genft_global['mixdb']['num_classes']))
    segsnr = to_numpy_array(mp_segsnr, dtype=np.single)

    sample_indices = slice(record['i_sample_offset'], record['i_sample_offset'] + record['samples'])
    frame_indices = slice(record['i_frame_offset'],
                          record['i_frame_offset'] + record['samples'] // genft_global['mixdb']['frame_size'])

    (mixture_td,
     truth_t[sample_indices],
     _,
     _,
     segsnr[frame_indices]) = get_audio_and_truth_t(mixdb=genft_global['mixdb'],
                                                    record=record,
                                                    target_audios=genft_global['target_audios'],
                                                    noise_audios=genft_global['noise_audios'],
                                                    compute_truth=True,
                                                    compute_segsnr=genft_global['compute_segsnr'],
                                                    frame_based=True)

    for frame in range(record['samples'] // genft_global['mixdb']['frame_size']):
        indices = slice(frame * genft_global['mixdb']['frame_size'], (frame + 1) * genft_global['mixdb']['frame_size'])
        mixture[frame + record['i_frame_offset']] = fft.execute(int16_to_float(mixture_td[indices]))


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']
        mixdb_name = args['--mixdb']
        mixid_name = args['--mixid']
        output_name = args['--output']
        compute_segsnr = args['--segsnr']

        if not output_name:
            output_name = splitext(mixdb_name)[0] + '.h5'

        start_time = time.monotonic()

        log_name = 'genft.log'
        create_file_handler(log_name)
        update_console_handler(verbose)
        initial_log_messages('genft')

        mixdb = load_mixdb(name=mixdb_name)
        mixid = load_mixid(name=mixid_name, mixdb=mixdb)

        mixdb_out, total_samples, transform_frames, feature_frames = init(mixdb=mixdb,
                                                                          mixid=mixid,
                                                                          logging=True)

        if not audio_files_exist(mixdb):
            raise SystemExit(1)

        fg = FeatureGenerator(frame_size=mixdb_out['frame_size'],
                              feature_mode=mixdb_out['feature'],
                              num_classes=mixdb_out['num_classes'],
                              truth_mutex=mixdb_out['truth_mutex'])

        chunk_size = 100
        progress = tqdm(total=len(mixid), desc='genft')
        mixid = grouper(range(len(mixdb_out['mixtures'])), chunk_size)
        mixdb_out['class_count'] = [0] * mixdb_out['num_classes']

        i_frame_offset = 0
        o_frame_offset = 0
        feature_elems = 0
        truth_elems = 0
        with h5py.File(output_name, 'w') as f:
            feature_dataset = f.create_dataset(name='feature',
                                               shape=(feature_frames, fg.stride, fg.num_bands),
                                               dtype=np.single)
            truth_dataset = f.create_dataset(name='truth_f',
                                             shape=(feature_frames, fg.num_classes),
                                             dtype=np.single)
            if compute_segsnr:
                segsnr_dataset = f.create_dataset(name='segsnr',
                                                  shape=(transform_frames,),
                                                  dtype=np.single)
            for m in mixid:
                feature, truth_f, segsnr, mixdb_tmp = genft(mixdb=mixdb_out,
                                                            mixid=m,
                                                            compute_segsnr=compute_segsnr,
                                                            logging=False,
                                                            progress=progress)
                o_frames = feature.shape[0]
                if o_frames != truth_f.shape[0]:
                    logger.exception(f'truth_f frames does not match feature frames: {truth_f.shape[0]} != {o_frames}')
                    raise SystemExit(1)

                indices = slice(o_frame_offset, o_frame_offset + o_frames)
                feature_dataset[indices] = feature
                truth_dataset[indices] = truth_f
                o_frame_offset += o_frames

                if compute_segsnr:
                    segsnr_dataset[i_frame_offset:i_frame_offset + segsnr.shape[0]] = segsnr
                    i_frame_offset += segsnr.shape[0]

                for idx, val in enumerate(m):
                    mixdb_out['mixtures'][val] = mixdb_tmp['mixtures'][idx]
                for idx in range(mixdb_out['num_classes']):
                    mixdb_out['class_count'][idx] += mixdb_tmp['class_count'][idx]
            f.attrs['mixdb'] = json.dumps(mixdb_out)
        progress.close()

        logger.info(f'Wrote {output_name}')
        duration = total_samples / sonusai.mixture.sample_rate
        logger.info('')
        logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
        logger.info(f'feature:  {human_readable_size(o_frame_offset * fg.stride * fg.num_bands * 4, 1)}')
        logger.info(f'truth_f:  {human_readable_size(o_frame_offset * fg.num_classes * 4, 1)}')
        if compute_segsnr:
            logger.info(f'segsnr:   {human_readable_size(i_frame_offset * 4, 1)}')

        end_time = time.monotonic()
        logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
