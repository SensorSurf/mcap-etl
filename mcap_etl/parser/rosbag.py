import pandas as pd

from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from rosbags.typesys import get_types_from_msg, register_types
from rosbags.typesys.base import Nodetype
from rosbags.typesys.types import FIELDDEFS


SEPARATOR = "__"


class FlatField:

    def __init__(self, name, ros_type):
        self.name = name
        self.ros_type = ros_type


class Topic:

    @staticmethod
    def format_name(name):
        if name.startswith('/'):
            name = name[1:]
        return name.replace('/', SEPARATOR)

    def __init__(self, name, schema):
        self.name = self.format_name(name)
        self.schema = schema
        self.__messages = list()
    
    def as_df(self):
        flattened = pd.json_normalize(self.__messages, sep=SEPARATOR)
        return pd.DataFrame(flattened)

    def add_message(self, message):
        self.__messages.append(message)

    def message_count(self):
        return len(self.__messages)


class RosbagParser:

    MS_IN_NS = 1e-6

    @staticmethod
    def is_rosbag(file):
        return file.endswith('.bag')

    def __init__(self, file):
        if not RosbagParser.is_rosbag(file):
            raise TypeError(f'Not a rosbag file: {file}')

        self.__file = file
        self.__topics = dict()
        self.__types = dict()
        
        for topic in self.__parse_topics(file):
            self.__topics[topic.name] = topic

    def read_message(self):
        with Reader(self.__file) as reader:
            for conn, ts, data in reader.messages():
                topic = Topic.format_name(conn.topic)

                msg = ros1_to_cdr(data, conn.msgtype)
                msg = deserialize_cdr(msg, conn.msgtype)
                msg = self.__filter_nonscalars(msg.__dict__)

                msg['ts'] = int(ts * self.MS_IN_NS)
                del msg['__msgtype__']

                yield topic, msg
                
    def read_messages(self):
        for topic, msg in self.read_message():
            self.__topics[topic].add_message(msg)
    
    def topics(self):
        return self.__topics.values()
    
    def __parse_topics(self, file):
        topics = list()
        with Reader(file) as reader:
            for conn in reader.connections:
                types = get_types_from_msg(conn.msgdef, conn.msgtype)
                register_types(types)
                self.__types.update(types)

                schema = self.__flatten_schema(conn.msgtype)

                topic = Topic(conn.topic, schema)
                topics.append(topic)
        return topics

    def __filter_nonscalars(self, data):
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = self.__filter_nonscalars(v)
        elif isinstance(data, (list, tuple)):
            for i, v in enumerate(data):
                data[i] = self.__filter_nonscalars(v)
        elif not isinstance(data, (int, float, bool, str, type(None))):
            return None

        return data

    def __flatten_schema(self, ros_type):
        ros_schema = self.__types.get(ros_type) or FIELDDEFS.get(ros_type)
        if ros_schema is None:
            raise TypeError(f'Unregistered ROS type: {ros_type}')

        schema_tree = ros_schema[1]
        flat_schema = list()

        for field_node in schema_tree:
            name = field_node[0]
            ros_type = field_node[1][1]

            is_prim = field_node[1][0] == Nodetype.BASE
            has_children = field_node[1][0] == Nodetype.NAME

            if is_prim:
                field = FlatField(name, ros_type)
                flat_schema.append(field)
            elif has_children:
                parent_prefix = name + SEPARATOR
                children = self.__flatten_schema(ros_type)
                for child in children:
                    full_name = parent_prefix + child.name
                    field = FlatField(full_name, child.ros_type)
                    flat_schema.append(field)

        return flat_schema
