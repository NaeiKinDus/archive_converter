# -*- coding: utf-8 -*-
# Tests includes/common.py
from pytest import mark
from typing import Union

from archiveconverter.includes.common \
    import get_files, generate_filename, strip_accents, run_command
from .config import get_files_data, generate_filename_data


@mark.parametrize("test_dir,expected", get_files_data)
def test_get_files(test_dir: str, expected: dict):
    found_files = get_files(test_dir)
    assert expected == found_files


@mark.parametrize("cli_args,extension,source,cont_dir,expected", generate_filename_data)
def test_generate_filename(cli_args: dict, extension: str, source: str, cont_dir: str, expected: Union[dict, type]):
    try:
        generated = generate_filename(cli_args, extension, source, cont_dir)
    except Exception as e:
        assert isinstance(e, expected)
    else:
        assert generated == expected


def test_strip_accents():
    assert strip_accents('Úŷàêñ€łäǫ¸ȩıỏ') == 'Uyaenao eo'


def test_run_command():
    for verbosity in [False, True]:
        for command in ['ls -lah', ['ls', '-lah']]:
            ret_code, ret_str = run_command(command, verbosity)
            assert ret_code == 0
            if not verbosity:
                assert not ret_str
            else:
                assert ret_str
