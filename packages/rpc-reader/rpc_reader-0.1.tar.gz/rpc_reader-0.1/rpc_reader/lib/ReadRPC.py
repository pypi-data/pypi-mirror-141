#!/bin/python3
import os
import pathlib
import struct
import sys
from copy import deepcopy

from rpc_reader.lib.print_progressbar import print_progressbar

# Define custom error
import numpy


class ReadRpcError(Exception):
    pass


class JobFileHeaderError(ReadRpcError):

    def __init__(self, job_file, expected_header, message='The PRC test data _file header is invalid'):
        self.job_file = job_file
        self.expected_header = expected_header
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f' In the job _file {self.job_file.as_posix} the expected header {self.expected_header} was not found'


class JobFileError(ReadRpcError):

    def __init__(self, job_file, message='The PRC test data _file is invalid'):
        self.job_file = job_file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if not isinstance(self.job_file, pathlib.Path):
            return 'Job must be supplied as pahtlib.Path object'
        elif not self.job_file.is_file():
            return f'The job _file was not found at expected path \n\t {self.job_file.as_posix()}'
        else:
            return 'An other problem with the job _file was encountered... sorry!'


class ReadRPC(object):
    """
    Read RPC III files.
    A RPC III _file is a data _file conforming to the RPC III _file specification developed by MTS corporation.

    In this implementation the full data structure of the PRC file is NOT supported.

    TODO:
        Support demultiplexed data format. Here it is assumed that only one frame exist in every group but this is
        generally not the case.

    Niklas Melin
    2022-02-26
    """

    def __init__(self, _file, debug=False):

        self.debug = debug
        self.headers = dict()
        self.channels = dict()
        self.data = None
        self.time = None
        self.__file_size__ = None
        self.__headers_read__ = False
        self.__data_read__ = False

        # Standard integer full scale
        self.integer_standard_full_scale = 32768

        # Check received _file
        if not isinstance(_file, pathlib.Path):
            _file = pathlib.Path(_file)
        if not _file.is_file():
            ReadRpcError(_file)
        self.file = _file

        # Open _file handle
        with open(self.file, 'rb') as file_handle:
            # Get _file size
            file_handle.seek(0, os.SEEK_END)
            self.__file_size__ = file_handle.tell()

            # Reposition to start of _file
            file_handle.seek(0, 0)

    def __read_header__(self, file_handle):

        def __header__():
            # Read header
            __head__, __value__ = struct.unpack('<32s96s', file_handle.read(128))
            __value__ = __value__.rstrip(b'\0').decode('utf-8')
            __head__ = __head__.rstrip(b'\0').decode('utf-8')
            return __head__, __value__

        # Read first three records, which are mandatory and also position sensitive
        print(f' Reading headers from:\n\tFile: {self.file.as_posix()}')
        for expected_header in ['FORMAT', 'NUM_HEADER_BLOCKS', 'NUM_PARAMS']:
            head_name, head_value = __header__()
            if not expected_header == head_name:
                raise JobFileHeaderError(file_handle, expected_header)
            if head_name in ['NUM_HEADER_BLOCKS', 'NUM_PARAMS']:
                self.headers[head_name] = int(head_value)
            else:
                self.headers[head_name] = head_value
            if self.debug:
                print(f'\t {head_name:18s}: {head_value}')

        # Check if _file contains data
        if not self.headers['NUM_PARAMS'] > 3:
            sys.exit('ERROR: No data in _file')

        # Read all remaining headers
        for channel in range(self.headers['NUM_PARAMS'] - 1):
            head_name, head_value = __header__()
            # Stored in blocks of 4 (512 bytes divided into 128 byte chunks), hence at the end empty headers can appear
            if len(head_name) != 0:
                self.headers[head_name] = head_value
                if self.debug:
                    print(f"\t\t {head_name:32s}  -- {head_value}")

        # Set current position in _file
        self.header_end = file_handle.tell()

        # Convert values to correct types
        try:
            self.headers['CHANNELS'] = int(self.headers['CHANNELS'])
            self.headers['DELTA_T'] = float(self.headers['DELTA_T'])
            self.headers['PTS_PER_FRAME'] = int(self.headers['PTS_PER_FRAME'])
            self.headers['PTS_PER_GROUP'] = int(self.headers['PTS_PER_GROUP'])
            self.headers['FRAMES'] = int(self.headers['FRAMES'])
            self.headers['INT_FULL_SCALE'] = int(self.headers['INT_FULL_SCALE'])
        except KeyError as expected_header:
            JobFileHeaderError(file_handle, expected_header)

        # Structure channel data structure
        for channel in range(int(self.headers['CHANNELS'])):
            try:
                self.channels[channel] = {}
                self.channels[channel]['Channel'] = 'Channel_' + repr(channel + 1).zfill(3)
                self.channels[channel]['Description'] = self.headers['DESC.CHAN_' + repr(channel + 1)]
                self.channels[channel]['LowerLimit'] = self.headers['LOWER_LIMIT.CHAN_' + repr(channel + 1)]
                self.channels[channel]['Scale'] = float(self.headers['SCALE.CHAN_' + repr(channel + 1)])
                self.channels[channel]['Units'] = self.headers['UNITS.CHAN_' + repr(channel + 1)]
                self.channels[channel]['UpperLimit'] = self.headers['UPPER_LIMIT.CHAN_' + repr(channel + 1)]
                if 'PART.NCHAN_' + repr(channel + 1) in self.headers:
                    self.channels[channel]['NumberInPartition'] = self.headers['PART.NCHAN_' + repr(channel + 1)]
            except KeyError as missing_key:
                print(f' Skipping: {missing_key}')
                continue

        # Indicate that the header was successfully read
        self.__headers_read__ = True

    def __read_data__(self, file_handle):
        if not self.__headers_read__:
            print(' ERROR: No header has been read, hence data structure unknown!')
            return

        channels = self.headers['CHANNELS']
        point_per_frame = self.headers['PTS_PER_FRAME']
        point_per_group = self.headers['PTS_PER_GROUP']
        frames = self.headers['FRAMES']
        print(f'\tChannels to read: {channels},\n'
              f'\tPoints per frame: {point_per_frame},\n'
              f'\tPoints per group: {point_per_group},\n'
              f'\tNumber of frames: {frames}')

        # Pre-allocate a numpy array
        self.data = numpy.zeros([frames * point_per_frame, channels])

        # Read after end of header
        file_handle.seek(self.header_end, 0)
        print(f'\tHeader end at {self.header_end} bytes')

        print(f'\n Reading test data from {channels} channels,')
        print_progressbar(0, frames, prefix='Progress:', suffix='Complete', length=50)

        for frame in range(frames):
            # print(f'\t Frame: {frame + 1} of {frames}')
            for channel in range(32):
                data = struct.unpack(f'<{point_per_group}h', file_handle.read(point_per_group * 2))

                r1 = frame * point_per_group
                r2 = (frame + 1) * point_per_group

                self.data[r1:r2, channel] = data
            print_progressbar(frame + 1, frames, prefix='Progress:', suffix='Complete', length=50)

        # Verify that all data in the file has been read
        if file_handle.tell() != self.__file_size__:
            message = f"ERROR: Data read does not match file length." \
                      f" Data read: {file_handle.tell()} bytes and file size {self.__file_size__} bytes does not match"
            raise JobFileError(self.file, message=message)

        # Copy data structure prior to applying scaling for __create_actuals_data_file__ purposes to ve
        if self.debug:
            self.data2 = deepcopy(self.data)

        # Scale channel data
        for channel in range(channels):
            # Channel scale
            channel_scale = self.channels[channel]['Scale']
            # Standard integer full scale
            int_standard_full_scale = self.integer_standard_full_scale
            # RPC integer full scale
            int_rpc_full_scale = self.headers['INT_FULL_SCALE']

            if self.debug:
                print(f'Channel {channel}, channel_scale:{channel_scale} {type(channel_scale)},'
                      f' int_standard_full_scale: {int_standard_full_scale} {type(int_standard_full_scale)},'
                      f' int_rpc_full_scale: {int_rpc_full_scale} {type(int_rpc_full_scale)}')

            # Compute scale factor
            scale_factor = int_rpc_full_scale / int_standard_full_scale * channel_scale

            # Scale data
            self.data[:, channel] = self.data[:, channel] * scale_factor

        # Create matching time history array
        self.time = numpy.arange(1, frames * point_per_frame + 1, dtype=numpy.float32) * self.headers['DELTA_T']

        # Indicate that the data has been read
        self.__data_read__ = True

    def import_rpc_data_from_file(self):

        # Open _file handle
        with open(self.file, 'rb') as file_handle:
            # Read headers
            self.__read_header__(file_handle)
            # Read data
            self.__read_data__(file_handle)

    def save_npy_data_to_file(self, overwrite=False):

        file_path_data = self.file.with_suffix('.npz')

        if file_path_data.is_file() and not overwrite:
            print(f' ERROR: A _file exists and over write mode is: {overwrite}')
            return
        data = self.data
        times = self.time
        headers = self.headers
        channels = self.channels
        numpy.savez(file_path_data,
                    data=data,
                    time=times,
                    headers=headers,
                    channels=channels)

        print(f' Data was exported to _file: {file_path_data.as_posix()}')

    def import_npy_data_from_file(self):

        #
        file_path_data = self.file.with_suffix('.npz')

        if not file_path_data.is_file():
            print(f' ERROR: Numpy .npz was not found: {file_path_data.as_posix()}')
            return

        npz_file = numpy.load(file_path_data, allow_pickle=True)
        self.data = npz_file['data']
        self.time = npz_file['time']
        self.headers = npz_file['headers']
        self.channels = npz_file['channels']

        print(f' Imported data of sizes: \n\tdata: {self.data.shape}\n\ttime: {self.time.shape}')

        # Set data available
        self.__data_read__ = True
        self.__headers_read__ = True

        print(f' Data was imported from _file: {file_path_data.as_posix()}')

    def get_data(self):
        if not self.__data_read__:
            print('ERROR: No data has been read!')
            return False
        return self.data

    def get_time(self):
        if not self.__data_read__:
            print('ERROR: No data has been read!')
            return False

        return self.time, self.time[-1]

    def get_data_size(self):
        if not self.__data_read__:
            print('ERROR: No data has been read!')
            return False
        return self.data.shape

    def get_channels(self):
        if not self.__headers_read__:
            print(' ERROR: No data loaded')
            return False
        return self.channels

    def get_headers(self):
        if not self.__headers_read__:
            print(' ERROR: No data loaded')
            return False
        return self.headers

    def print_channel_header_data(self):
        if not self.__headers_read__:
            print(' ERROR: No data loaded')
            return

        for channel, data in self.channels.items():
            print(f' Channel: {channel + 1}')
            for key, value in data.items():
                print(f' \t {key:20s} : {value}')


def main(test_data_file):

    test_data_file = pathlib.Path(test_data_file)
    print(f' Reading data from _file: \n\t{test_data_file.as_posix()}\n')
    data_object = ReadRPC(test_data_file)

    data_object.print_channel_header_data()

    samples, channels = data_object.get_data_size()

    time_array, test_end_time = data_object.get_time()

    print(f'\n Test data points read:\n\tChannels: {channels}'
          f'\n\tSamples:  {samples}'
          f'\n\tDuration: {test_end_time} seconds')


if __name__ == "__main__":
    file = sys.argv[1]
    print(' Not completed yet...')
