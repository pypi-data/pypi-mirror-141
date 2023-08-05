import datetime
import multiprocessing
import random
from multiprocessing import Manager
from typing import List
from typing import Union

import numpy as np
from tensorflow.keras.utils import Sequence

from sonusai import SonusAIError
from sonusai import logger
from sonusai.genft import genft
from sonusai.mixture import get_mixtures_from_mixid
from sonusai.utils import reshape_inputs


class DataGenerator(Sequence):
    """Generates data for Keras"""

    def __init__(self,
                 mixdb: dict,
                 mixid: Union[str, List[int]],
                 batch_size: int,
                 timesteps: int,
                 flatten: bool,
                 add1ch: bool,
                 shuffle: bool = False,
                 chunks: int = 16):
        """Initialization"""
        self.mixdb = mixdb
        self.mixid = mixid
        self.batch_size = batch_size
        self.timesteps = timesteps
        self.flatten = flatten
        self.add1ch = add1ch
        self.shuffle = shuffle
        self.chunks = chunks

        self.index_map = None
        self.total_batches = None
        self.frames_per_batch = None
        self.cache_misses = list()
        self.debug = False
        self.fetching = multiprocessing.Condition()

        manager = Manager()
        self.data = manager.dict()

        self.initialize_mixtures()

    def __len__(self):
        """Denotes the number of batches per epoch"""
        return self.total_batches

    def __getitem__(self, batch_index: int):
        """Generate one batch of data"""
        with self.fetching:
            if batch_index not in self.data:
                self.fetch_data_for_index(batch_index)
                if self.debug:
                    logger.debug(f'\nTRACE {datetime.datetime.now()} fetch {batch_index:3d} {list(self.data.keys())}')
            else:
                if self.debug:
                    logger.debug(f'\nTRACE {datetime.datetime.now()} cache {batch_index:3d} {list(self.data.keys())}')

            feature = self.data[batch_index]['feature']
            truth = self.data[batch_index]['truth']
            del self.data[batch_index]

        feature, truth, _, _, _, _ = reshape_inputs(feature=feature,
                                                    truth=truth,
                                                    batch_size=self.batch_size,
                                                    timesteps=self.timesteps,
                                                    flatten=self.flatten,
                                                    add1ch=self.add1ch)

        return feature, truth

    def on_epoch_end(self):
        """Modification of dataset between epochs"""
        if self.shuffle:
            random.shuffle(self.mixid)
            self.initialize_mixtures()

    def get_feature_frames(self, mixtures: list, mixid: Union[str, List[int]] = ':', start_offset: int = 0) -> int:
        subset = get_mixtures_from_mixid(mixtures, mixid)
        return sum([sub['samples'] for sub in subset]) // self.mixdb['feature_step_samples'] - start_offset

    def initialize_mixtures(self):
        self.mixdb['mixtures'] = get_mixtures_from_mixid(self.mixdb['mixtures'], self.mixid)

        frames = self.get_feature_frames(self.mixdb['mixtures'])
        self.frames_per_batch = self.batch_size if self.timesteps == 0 else self.batch_size * self.timesteps
        self.total_batches = frames // self.frames_per_batch

        if self.total_batches == 0:
            logger.error(
                f'Error: dataset only contains {frames} frames which is not enough to fill a batch size of '
                f'{self.features_per_batch}. Either provide more data or decrease the batch size')
            raise SonusAIError

        # Compute mixid and offset for dataset
        # offsets are needed because mixtures are not guaranteed to fall on batch boundaries.
        # When fetching a new index that starts in the middle of a sequence of mixtures, the
        # previous feature frame offset must be maintained in order to preserve the correct
        # data sequence.
        cumulative_samples = np.cumsum([sub['samples'] for sub in self.mixdb['mixtures']])
        offsets = cumulative_samples // self.mixdb['feature_step_samples'] - 1
        self.index_map = [dict() for _ in range(self.total_batches)]
        cur_offset = 0
        prv_id = 0
        for n in range(self.total_batches):
            mixid = list()
            offset = list()
            for batch_index in range(n * self.frames_per_batch, (n + 1) * self.frames_per_batch):
                cur_id = next(idx for idx, val in enumerate(offsets) if val >= batch_index)
                if cur_id != prv_id:
                    cur_offset = 0
                offset.append(cur_offset)
                cur_offset += 1
                prv_id = cur_id
                mixid.append(cur_id)
            mixid = sorted(list(set(mixid)))

            self.index_map[n]['mixid'] = mixid
            self.index_map[n]['offset'] = offset

    def fetch_data_for_index(self, batch_index: int):
        self.cache_misses.append(batch_index)

        # Don't skip any indices when filling cache
        if len(self.data) > 0:
            next_cached_index = list(self.data.keys())[-1] + 1
            if batch_index > next_cached_index:
                batch_index = next_cached_index

        # Always fetch starting at a chunk boundary
        batch_index = (batch_index // self.chunks) * self.chunks

        mixid = self.index_map[batch_index]['mixid']
        offset = self.index_map[batch_index]['offset'][0]
        chunks = self.get_feature_frames(mixtures=self.mixdb['mixtures'],
                                         mixid=mixid,
                                         start_offset=offset) // self.frames_per_batch
        while chunks < self.chunks and mixid[-1] < len(self.mixdb['mixtures']) - 1:
            mixid.append(mixid[-1] + 1)
            chunks = self.get_feature_frames(mixtures=self.mixdb['mixtures'],
                                             mixid=mixid,
                                             start_offset=offset) // self.frames_per_batch

        feature, truth, _, _ = genft(mixdb=self.mixdb,
                                     mixid=mixid,
                                     start_offset=offset,
                                     logging=False,
                                     parallel=False)

        frames = (feature.shape[0] // self.frames_per_batch) * self.frames_per_batch
        batches = frames // self.frames_per_batch

        if batches == 0:
            logger.error(
                f'Error: genft returned {feature.shape[0]} frames which is not enough to fill a batch size of '
                f'{self.features_per_batch}. Either provide more data or decrease the batch size')
            raise SonusAIError

        feature = feature[:frames].reshape((batches, self.frames_per_batch, feature.shape[1], feature.shape[2]))
        truth = truth[:frames].reshape((batches, self.frames_per_batch, truth.shape[1]))

        # Add new values to data cache
        for index in range(batches):
            self.data[batch_index + index] = {'feature': feature[index], 'truth': truth[index]}

    def get_cache_misses(self):
        return self.cache_misses
