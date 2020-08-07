# -*- coding: utf-8 -*-
# Tests includes/arc.py
from natsort import natsorted, ns
from os import path, unlink, mkdir
from pytest import mark, fixture
from shutil import move, rmtree
from typing import Optional, Any, Callable, List, Tuple
import zipfile

from archiveconverter.includes.common import get_files, run_command
from archiveconverter.includes.arc import create_cbz, unpack_cbz,\
    create_cbr, unpack_cbr, RAR_BIN
from .config import get_files_data, OUTPUT_DIR, unpack_cbz_data, unpack_cbr_data


@fixture(autouse=True)
def dir_cleanup():
    """
    Empties the output directory between tests
    :return:
    """
    rmtree(OUTPUT_DIR)
    mkdir(OUTPUT_DIR)


def assert_create_defs(create_def: Callable, assert_def: Callable, extension: str, files_layout: dict):
    """
    Tests run for archive creation
    :param create_def: callable to test the creation process
    :type create_def: callable
    :param assert_def: callable to test the created archive
    :type assert_def: callable
    :param extension: type of the archive
    :type extension: str
    :param files_layout: source files used for the test
    :type files_layout: dict
    :return:
    """
    for arc_dir, data in files_layout.items():
        generated_zip = create_def(data['files_list'])
        assert generated_zip
        assert path.isfile(generated_zip)
        target_file = '{}/{}.{}'.format(OUTPUT_DIR, data['dir'], extension)
        move(generated_zip, target_file)
        assert path.isfile(target_file)
        source_list = list(map(lambda x: x[0], data['files_list']))
        source_list = natsorted(source_list, alg=ns.IGNORECASE)
        assert_def(target_file, source_list)
        try:
            unlink(target_file)
        except FileNotFoundError:
            pass


def assert_cbz(target_file: str, expected_list: List[Tuple[str, str]]):
    """
    Check created archive's content
    :param target_file: CBZ archive
    :type target_file: str
    :param expected_list: files expected to be in the archive
    :type expected_list: list
    :return: None
    """
    assert zipfile.is_zipfile(target_file)
    with zipfile.ZipFile(target_file, 'r') as source_zip:
        assert not source_zip.testzip()
        source_list = source_zip.namelist()
        source_list = natsorted(source_list, alg=ns.IGNORECASE)
    assert source_list == expected_list


def assert_cbr(target_file: str, expected_list: List[Tuple[str, str]]):
    """
    Check created archive's content
    :param target_file: CBR archive
    :type target_file: str
    :param expected_list: files expected to be in the archive
    :type expected_list: list
    :return: None
    """
    assert run_command([RAR_BIN, 't', target_file]) == (0, '')
    assert run_command([RAR_BIN, 'e', target_file, OUTPUT_DIR]) == (0, '')
    extracted = list(
        x for x in map(
            lambda x: x[0],
            get_files(OUTPUT_DIR)[OUTPUT_DIR]['files_list']
        ) if x != path.split(target_file)[-1]
    )

    assert extracted == expected_list
    for item in extracted:
        unlink(path.join(OUTPUT_DIR, item))


@mark.parametrize("test_dir,files_layout", get_files_data)
def test_create_cbz(test_dir: str, files_layout: dict):
    assert_create_defs(create_cbz, assert_cbz, 'cbz', files_layout)


@mark.parametrize("test_dir,files_layout", get_files_data)
def test_create_cbr(test_dir: str, files_layout: dict):
    assert_create_defs(create_cbr, assert_cbr, 'cbr', files_layout)


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
        unpacked_list = natsorted(unpacked_list, alg=ns.IGNORECASE)
        assert unpacked_list == file_list
        rmtree(unpack_dir)


@mark.parametrize("source_file,destination,lambda_validator,file_list", unpack_cbr_data)
def test_unpack_cbr(source_file: str, destination: Optional[dict], lambda_validator: Any, file_list: Optional[list]):
    try:
        unpack_dir = unpack_cbr(source_file, destination)
    except Exception as e:
        assert lambda_validator(e)
    else:
        assert lambda_validator(unpack_dir)
        assert path.isdir(unpack_dir)
        unpacked_files = get_files(unpack_dir)
        unpacked_list = list(map(lambda x: x[0], unpacked_files.popitem()[1]['files_list']))
        unpacked_list = natsorted(unpacked_list, alg=ns.IGNORECASE)
        assert unpacked_list == file_list
        rmtree(unpack_dir)
