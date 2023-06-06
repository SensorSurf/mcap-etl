#!/usr/bin/env python

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcap_etl.timescale import executor as timescale
from mcap_etl.convert import executor as convert


TIMESCALE = 'timescale'
CONVERT = 'convert'

def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='actions', dest='action')

    timescale_parser = subparsers.add_parser(TIMESCALE, help='Transform rosbag or mcap file into timescale database')
    timescale_parser.add_argument("-g", "--host", default='localhost', help="Postgres host")
    timescale_parser.add_argument("-p", "--port", default='5432', help="Postgres port")
    timescale_parser.add_argument("-u", "--user", default='postgres', help="Postgres user")
    timescale_parser.add_argument("-w", "--password", default='password', help="Postgres password")
    timescale_parser.add_argument("-n", "--name", default='postgres', help="Postgres database name")

    rosbag_parser = subparsers.add_parser(CONVERT, help='Convert mcap file into rosbag file')
    rosbag_parser.add_argument("-o", "--output", help='Output rosbag file path')

    parser.add_argument("file", help="Path to rosbag or mcap file")

    args = parser.parse_args()

    if args.action == TIMESCALE:
        timescale.run(args.file, args.host, args.port, args.user, args.password, args.name)
    elif args.action == CONVERT:
        convert.run(args.file, args.output)

if __name__ == "__main__":
    main()
