from .postgres import TimescaleWrapper

from ..convert.mcap import McapConverter
from ..parser.rosbag import RosbagParser


def run(file, pg_host='localhost', pg_port='5432', pg_user='postgres', pg_pass='password', pg_name='postgres'):
    if not RosbagParser.is_rosbag(file):
        if McapConverter.is_mcap(file):
            print(f'Converting mcap to rosbag: file={file}')
            mcap_converter = McapConverter(file)
            file = mcap_converter.to_rosbag()
            print(f'Converted mcap to rosbag: file={file}')
        else:
            print(f'Not a rosbag or mcap file: file={file}')
            exit(1)

    rosbag_parser = RosbagParser(file)

    print(f'Establishing connection to database: host={pg_host}')
    timescale = TimescaleWrapper(pg_host, pg_port, pg_user, pg_pass, pg_name)

    print(f'Reading messages from rosbag: file={file}')
    rosbag_parser.read_messages()

    for topic in rosbag_parser.topics():
        name = topic.name
        fields = topic.schema

        if not timescale.exists(name):
            print(f'Creating: table={name}')
            timescale.create(name, fields)
        else:
            old_cols = set(timescale.columns(name))
            new_cols = [field for field in fields if field.name not in old_cols]

            if len(new_cols) > 0:
                formatted_new_cols = ','.join([col.name for col in new_cols])
                print(f'Adding columns: table={name}, new_columns={formatted_new_cols}')

                timescale.update(name, new_cols)

        print(f'Inserting records: table={name}, count={topic.message_count()}')
        timescale.insert(name, topic.as_df())
