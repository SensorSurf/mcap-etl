from mcap.reader import make_reader
from rosbags.rosbag1 import Writer
from rosbags.serde import cdr_to_ros1
from rosbags.typesys import get_types_from_msg, register_types


class McapConverter:

    @staticmethod
    def is_mcap(file):
        return file.endswith('.mcap')

    def __init__(self, mcap_file):
        if not McapConverter.is_mcap(mcap_file):
            raise ValueError(f'Not an mcap file: file={mcap_file}')

        self.__mcap_file = mcap_file
        self.__default_output_file = mcap_file.replace('.mcap', '.bag')
    
    def __message_generator(self):
        with open(self.__mcap_file, 'rb') as f:
            reader = make_reader(f)
            for schema, channel, message in reader.iter_messages():
                yield message.log_time, schema.name, schema.data.decode(), channel.topic, message.data
    
    def to_rosbag(self, output_file=None):
        output_file = output_file or self.__default_output_file

        with Writer(output_file) as w:
            conns = {}
            seen = set()

            for ts, ros_type, schema, topic, data in self.__message_generator():
                if ros_type not in seen:
                    seen.add(ros_type)
                    types = get_types_from_msg(schema, ros_type)
                    register_types(types)
                    conns[ros_type] = w.add_connection(topic, ros_type, schema)

                if ros_type in conns:
                    conn = conns[ros_type]
                    msg = cdr_to_ros1(data, ros_type)
                    w.write(conn, ts, msg)
        
        return output_file
