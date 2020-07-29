#!/usr/bin/python3
# -*- coding: utf-8 -*

import argparse
from includes.common import get_files, generate_filename,\
    allowed_archive_extensions as allowed_extensions
from includes.arc import ArchiveHandler
import os


def main(arguments):
    match_extension = allowed_extensions
    if arguments.source_extension:
        match_extension = arguments.source_extension.split(',')

    match_files = get_files(arguments.source, match_extension)
    arc_manager = ArchiveHandler(dry_run=arguments.dry_run)

    for current_dir, dir_info in match_files.items():
        for (filename, filepath) in dir_info['files_list']:
            #unpack_dir = unpack_archive(filepath)
            target_filename = generate_filename(arguments, filename, dir_info['dir'])
            target_destination = os.path.join(arguments.destination, target_filename)
            #pack_files(unpack_dir, target_destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repack comic archives to the specified type")
    parser.add_argument('source', type=str, metavar='source_directory')
    parser.add_argument('destination', type=str, metavar='destination_directory')
    parser.add_argument(
        '-se', '--source-extension', type=str, metavar='src_ext',
        help='match only files with the specified extension; use * to match all comic archive extensions.'
    )
    parser.add_argument(
        '-f', '--format', type=str, metavar='dst_format', default='cbz', choices=allowed_extensions,
        help='convert all matching archives to the selected archive type.'
    )
    parser.add_argument(
        '-rv', '--rar-version', metavar='version', type=int, default=4,
        help='select the archiving format version (see the -ma switch of the `rar` utility)'
    )
    args = parser.parse_args()

    if args.rar_version not in [4, 5]:
        parser.error('--rar-version supports version 4 or 5.')
    main(args)
