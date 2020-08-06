#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
from archiveconverter.includes.common import get_files, generate_filename, supported_naming_methods, \
    allowed_archive_extensions as allowed_extensions, strip_accents
from archiveconverter.includes.arc import ArchiveHandler
import os


repack_modes = [
    'one',
    'many'
]


def main(arguments):
    match_extension = allowed_extensions
    if arguments.source_extension and arguments.source_extension != '*':
        match_extension = arguments.source_extension.split(',')

    arc_manager = ArchiveHandler(dry_run=arguments.dry_run)

    for source_item in arguments.source:
        if os.path.isdir(source_item):
            match_files = get_files(source_item, match_extension)
        else:
            filename = os.path.split(source_item)[-1]
            source_dir = os.path.split(source_item)[0]
            match_files = {
                source_dir: {
                    'dir': source_item.split(os.path.sep)[-2],
                    'src': source_dir,
                    'files_list': [(filename, source_item)]
                }
            }
        for current_dir, dir_info in match_files.items():
            for (filename, filepath) in dir_info['files_list']:
                unpack_dir = arc_manager.unpack_archive(filepath)
                if arguments.naming_method == 'source_name':
                    target_filename = filename
                else:
                    target_filename = generate_filename(vars(arguments), arguments.archive_type, filename, dir_info['dir'])
                if arguments.strip_accents:
                    target_filename = strip_accents(target_filename)
                target_destination = os.path.join(arguments.destination, target_filename)
                unpacked_files = get_files(unpack_dir)
                for unpacked_source, files in unpacked_files.items():
                    arc_manager.pack_files(files['files_list'], target_destination)


"""
@todo support multiple source to multiple dest AND multiple source to a single archive
@todo support --mode
@todo support --in-place
@todo support --remove
@todo support --dry-run
@todo support --rar-version
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repack comic archives to the specified type")
    parser.add_argument(
        'source', type=str, metavar='source', nargs='+',
        help='file or directory where the source archives are located'
    )
    parser.add_argument(
        'destination', type=str, metavar='destination_directory',
        help='directory where the repacked files will be created'
    )
    # parser.add_argument(
    #     '-m', '--mode', type=str, metavar='repack_mode', choices=repack_modes, default='many',
    #     help='mode used to repack; all source in one archive, or each source in its own archive'
    # )
    parser.add_argument(
        '-ar', '--archive-type', type=str, metavar='extension', default='cbz', choices=allowed_extensions,
        help='convert all matching archives to the selected archive type.'
    )
    # parser.add_argument(
    #     '-rv', '--rar-version', metavar='version', type=int, default=4,
    #     help='select the archiving format version (see the -ma switch of the `rar` utility)'
    # )
    parser.add_argument(
        '-se', '--source-extension', type=str, metavar='src_ext', default='*',
        help='match only files with the specified extension; use * to match all comic archive extensions.'
    )
    parser.add_argument(
        '-sa', '--strip-accents', default=True, action='store_true',
        help='convert image filenames to non-accentuated chars, or strip them; some readers require this'
    )
    # parser.add_argument(
    #     '--in-place', default=False, action='store_true',
    #     help='the repacked archive will be in the same directory the source archive was'
    # )
    # parser.add_argument(
    #     '--remove', default=False, action='store_true',
    #     help='remove the source archive once it is repacked'
    # )
    naming_methods = list(supported_naming_methods.keys())
    naming_methods.append('source_name')
    parser.add_argument(
        '-nm', '--naming-method', type=str, choices=naming_methods, default='source_name',
        help='how the archive file name is generated'
    )
    parser.add_argument(
        '-nf', '--naming-format', type=str,
        help='string using variable replacement to generate an archive name when using the "context" naming method'
    )
    parser.add_argument(
        '-dr', '--dry-run', action='store_true',
        help='show what actions will be performed but do not execute them'
    )
    args = parser.parse_args()

    if args.rar_version not in [4, 5]:
        parser.error('--rar-version supports version 4 or 5.')
    main(args)
