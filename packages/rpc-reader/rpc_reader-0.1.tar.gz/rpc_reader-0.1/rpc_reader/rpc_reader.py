import sys
from rpc_reader.lib.ReadRPC import ReadRPC


def main():
    rpc_data_file = sys.argv[1]
    reader_object = ReadRPC(rpc_data_file)
    reader_object.save_npy_data_to_file()


if __name__ == '__main__':
    # Get current working directory
    file = sys.argv[1]
    ReadRPC(file)
