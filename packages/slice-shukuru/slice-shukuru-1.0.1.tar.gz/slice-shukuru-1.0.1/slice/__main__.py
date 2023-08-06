"""Slice entrypoint

Execute Slice CLI tool
"""

import argparse
import os

from humanfriendly import parse_size

from slice import slicing

if __name__ == '__main__':
    argp = argparse.ArgumentParser(
        prog="slice",
        description="Simple file splitter"
    )

    argp.version = 'v1.0.0'

    argp_mutex = argp.add_mutually_exclusive_group(required=True)

    argp.add_argument(
        'File',
        metavar='file',
        type=str,
        help='Path to file you want to be sliced'
    )

    argp.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Output process on stdout'
    )

    argp.add_argument(
        '-V',
        '--version',
        action='version',
        help='Output program version and exit'
    )

    argp_mutex.add_argument(
        '-s',
        '--size',
        metavar='CHUNK SIZE',
        action='store',
        type=str,
        help='Numeric or human-readable chunk size value (1024, 16MB, 1GiB, ...)',
    )

    argp_mutex.add_argument(
        '-c',
        '--count',
        metavar='PARTS COUNT',
        action='store',
        type=int,
        help='Total parts count to slice the file in'
    )

    args = argp.parse_args()

    # Stat file size
    file_size = os.stat(args.File).st_size

    # Open it
    with open(args.File, 'rb') as reader:
        # Slice by size mode
        if args.size:
            slicing.slice_by_size(
                reader,
                args.File,
                file_size,
                parse_size(args.size, binary=True)
            )
        # Slice by parts count mode
        if args.count:
            slicing.slice_by_count(
                reader,
                args.File,
                file_size,
                args.count
            )
