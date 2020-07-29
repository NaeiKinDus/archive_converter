#!/usr/bin/python3
# -*- coding: utf-8 -*

import argparse
from includes import common
from includes.arc import ArchiveHandler


def main(arguments):
    """
    Main function
    :param arguments: parsed CLI arguments
    :return: None
    """
    files_list = common.get_files(arguments.source, common.allowed_file_extensions)
    arc_manager = ArchiveHandler(dry_run=arguments.dry_run)

    for source, files in files_list.items():
        target_filename = common.generate_filename(arguments, arguments.archive_type, source, files['dir'])
        if arguments.dry_run:
            print('img_to_cbz: using target filename "{}"'.format(target_filename))
        arc_manager.pack_files(files['files_list'], target_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a bunch of images to a CBZ archive")
    parser.add_argument('source', type=str, metavar='dir')
    parser.add_argument('destination', type=str, metavar='dir')
    parser.add_argument(
        '-ar', '--archive-type', default='cbz', choices=common.allowed_archive_extensions, type=str, metavar="extension"
    )
    parser.add_argument('-nm', '--naming-method', type=str, choices=common.naming_methods.keys(), default='directory')
    parser.add_argument('-nf', '--naming-format', type=str)
    parser.add_argument('-dr', '--dry-run', action='store_true')
    args = parser.parse_args()

    if args.naming_method != 'directory' and not args.naming_format:
        parser.error('--naming-format is required if --naming-method is not set to `directory` (default)')
    common.DRY_RUN = args.dry_run

    main(args)
