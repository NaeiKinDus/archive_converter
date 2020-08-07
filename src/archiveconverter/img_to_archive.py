#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse

from archiveconverter.includes import common
from archiveconverter.includes.arc import ArchiveHandler


def main(arguments):
    """
    Main function
    :param arguments: parsed CLI arguments
    :return: None
    """
    files_list = common.get_files(arguments.source, common.allowed_file_extensions)
    arc_manager = ArchiveHandler(dry_run=arguments.dry_run)

    for source, files in files_list.items():
        target_filename = common.generate_filename(vars(arguments), arguments.archive_type, source, files['dir'])
        if arguments.strip_accents:
            target_filename = common.strip_accents(target_filename)
        if arguments.dry_run:
            print('img_to_archive: using target filename "{}"'.format(target_filename))
        arc_manager.pack_files(files['files_list'], target_filename)


"""
@todo support more format
@todo handle --dry-run
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a bunch of images to a CBZ archive")
    parser.add_argument(
        'source', type=str, metavar='dir',
        help='directory where the source images are located'
    )
    parser.add_argument(
        'destination', type=str, metavar='dir',
        help='directory where the archives will be created'
    )
    parser.add_argument(
        '-ar', '--archive-type', default='cbz', choices=common.allowed_archive_extensions, type=str, metavar="extension",
        help='Type of target archive',
    )
    parser.add_argument(
        '-nm', '--naming-method', type=str, choices=common.supported_naming_methods.keys(), default='directory',
        help='how the archive file name is generated'
    )
    parser.add_argument(
        '-sa', '--strip-accents', default=True, action='store_true',
        help='convert image filenames to non-accentuated chars, or strip them; some readers require this'
    )
    parser.add_argument(
        '-nf', '--naming-format', type=str,
        help='string using variable replacement to generate an archive name when using the "context" naming method'
    )
    # parser.add_argument(
    #     '-dr', '--dry-run', action='store_true',
    #     help='show what actions will be performed but do not execute them'
    # )
    args = parser.parse_args()

    if args.naming_method != 'directory' and not args.naming_format:
        parser.error('--naming-format is required if --naming-method is not set to `directory` (default)')
    common.DRY_RUN = args.dry_run
    main(args)
