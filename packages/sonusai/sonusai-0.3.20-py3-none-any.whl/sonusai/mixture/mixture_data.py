import numpy as np

from sonusai import SonusAIError
from sonusai import logger
from sonusai.mixture import apply_augmentation
from sonusai.mixture import generate_segsnr
from sonusai.mixture import generate_truth
from sonusai.mixture import get_next_noise
from sonusai.mixture import get_noise_audio_from_db
from sonusai.mixture import get_target_audio_from_db


def get_target_noise_audio(mixdb: dict,
                           record: dict,
                           target_audios: list,
                           noise_audios: list) -> (np.ndarray, np.ndarray):
    if record['samples'] % mixdb['frame_size'] != 0:
        logger.exception(f'Number of samples in record is not a multiple of {mixdb["frame_size"]}')
        raise SonusAIError
    target_file_index = record['target_file_index']
    target_augmentation = mixdb['target_augmentations'][record['target_augmentation_index']]
    target_audio = apply_augmentation(audio_in=get_target_audio_from_db(target_audios, target_file_index),
                                      augmentation=target_augmentation,
                                      length_common_denominator=mixdb['feature_step_samples'],
                                      dither=mixdb['dither'])
    if len(target_audio) != record['samples']:
        logger.exception('Number of samples in target does not match database')
        raise SonusAIError
    noise_file_index = record['noise_file_index']
    noise_augmentation_index = record['noise_augmentation_index']
    noise_audio, _ = get_next_noise(offset_in=record['noise_offset'],
                                    length=record['samples'],
                                    audio_in=get_noise_audio_from_db(noise_audios,
                                                                     noise_file_index,
                                                                     noise_augmentation_index))

    target_audio = np.array(np.single(target_audio) * record['target_snr_gain'], dtype=np.int16)
    noise_audio = np.array(np.single(noise_audio) * record['noise_snr_gain'], dtype=np.int16)

    return target_audio, noise_audio


def get_audio_and_truth_t(mixdb: dict,
                          record: dict,
                          target_audios: list,
                          noise_audios: list,
                          compute_truth: bool = True,
                          compute_segsnr: bool = False,
                          frame_based: bool = False) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    target, noise = get_target_noise_audio(mixdb=mixdb,
                                           record=record,
                                           target_audios=target_audios,
                                           noise_audios=noise_audios)

    mixture = np.array(target + noise, dtype=np.int16)

    truth_t = generate_truth(mixdb=mixdb,
                             record=record,
                             target=target,
                             noise=noise,
                             compute=compute_truth)

    segsnr = generate_segsnr(mixdb=mixdb,
                             record=record,
                             target=target,
                             noise=noise,
                             compute=compute_segsnr,
                             frame_based=frame_based)

    return mixture, truth_t, target, noise, segsnr


def set_mixture_offsets(mixdb: dict) -> None:
    i_sample_offset = 0
    i_frame_offset = 0
    o_frame_offset = 0
    for record in mixdb['mixtures']:
        record['i_sample_offset'] = i_sample_offset
        record['i_frame_offset'] = i_frame_offset
        record['o_frame_offset'] = o_frame_offset

        i_sample_offset += record['samples']
        i_frame_offset += record['samples'] // mixdb['frame_size']
        o_frame_offset += record['samples'] // mixdb['feature_step_samples']
