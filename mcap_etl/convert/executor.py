from .mcap import McapConverter


def run(input_file, output_file=None):
    if McapConverter.is_mcap(input_file):
        mcap_converter = McapConverter(input_file)
        print(f'Converting mcap to rosbag: file={input_file}')
        output_file = mcap_converter.to_rosbag(output_file)
        print(f'Converted mcap to rosbag: file={output_file}')
    else:
        print(f'Not an mcap file: file={input_file}')
        exit(1)
