# -*- coding: utf-8 -*-
# Tests includes/arc.py
from archiveconverter.includes.common import get_files
from archiveconverter.includes.arc import create_cbz, unpack_cbz
from os import path, unlink
from pytest import mark
from shutil import move, rmtree
from typing import Optional, Any
from .config import get_files_data, get_zip_file_list, OUTPUT_DIR,\
    unpack_cbz_data


@mark.parametrize("test_dir,files_layout", get_files_data)
def test_create_cbz(test_dir: str, files_layout: dict):
    for arc_dir, data in files_layout.items():
        generated_zip = create_cbz(data['files_list'])
        assert generated_zip
        assert path.isfile(generated_zip)
        target_file = '{}/{}.cbz'.format(OUTPUT_DIR, data['dir'])
        move(generated_zip, target_file)
        assert path.isfile(target_file)
        file_list = get_zip_file_list(target_file)
        source_list = list(map(lambda x: x[0], data['files_list']))
        source_list.sort()
        assert file_list == source_list
        unlink(target_file)


@mark.parametrize("source_file,destination,lambda_validator,file_list", unpack_cbz_data)
def test_unpack_cbz(source_file: str, destination: Optional[dict], lambda_validator: Any, file_list: Optional[list]):
    try:
        unpack_dir = unpack_cbz(source_file, destination)
    except Exception as e:
        assert lambda_validator(e)
    else:
        assert lambda_validator(unpack_dir)
        assert path.isdir(unpack_dir)
        unpacked_files = get_files(unpack_dir)
        unpacked_list = list(map(lambda x: x[0], unpacked_files.popitem()[1]['files_list']))
        unpacked_list.sort()
        assert unpacked_list == file_list
        rmtree(unpack_dir)


def test_create_cbr():
    pass


def test_unpack_cbr():
    pass
