# -*- coding: utf-8 -*-
# Test data and functions used by pytest

import zipfile


# Config parameters
OUTPUT_DIR = 'tests/output'


# Pytest data
get_files_data = [
    (
        'tests/images/single',
        {
            'tests/images/single': {
                'dir': 'single',
                'src': 'tests/images/single',
                'files_list': [
                    ['alphabet_d.png', 'tests/images/single/alphabet_d.png'],
                    ['alphabet_b.png', 'tests/images/single/alphabet_b.png'],
                    ['alphabet_c.png', 'tests/images/single/alphabet_c.png'],
                    ['alphabet_a.png', 'tests/images/single/alphabet_a.png']
                ]
            }
        },
    ),
    (
        'tests/images/multiple',
        {
            'tests/images/multiple/Book 2 - Numbers': {
                'dir': 'Book 2 - Numbers',
                'src': 'tests/images/multiple/Book 2 - Numbers',
                'files_list': [
                    ['number_6.png', 'tests/images/multiple/Book 2 - Numbers/number_6.png'],
                    ['number_1.png', 'tests/images/multiple/Book 2 - Numbers/number_1.png'],
                    ['number_4.png', 'tests/images/multiple/Book 2 - Numbers/number_4.png'],
                    ['number_3.png', 'tests/images/multiple/Book 2 - Numbers/number_3.png'],
                    ['number_9.png', 'tests/images/multiple/Book 2 - Numbers/number_9.png'],
                    ['number_7.png', 'tests/images/multiple/Book 2 - Numbers/number_7.png'],
                    ['number_2.png', 'tests/images/multiple/Book 2 - Numbers/number_2.png'],
                    ['number_8.png', 'tests/images/multiple/Book 2 - Numbers/number_8.png'],
                    ['number_5.png', 'tests/images/multiple/Book 2 - Numbers/number_5.png'],
                    ['number_10.png', 'tests/images/multiple/Book 2 - Numbers/number_10.png']
                ]
            },
            'tests/images/multiple/sub/Book 3 - Animals': {
                'dir': 'Book 3 - Animals',
                'src': 'tests/images/multiple/sub/Book 3 - Animals',
                'files_list': [
                    ['dog.png', 'tests/images/multiple/sub/Book 3 - Animals/dog.png'],
                    ['hummingbird.png', 'tests/images/multiple/sub/Book 3 - Animals/hummingbird.png'],
                    ['monkey.png', 'tests/images/multiple/sub/Book 3 - Animals/monkey.png'],
                    ['dog_cat.png', 'tests/images/multiple/sub/Book 3 - Animals/dog_cat.png'],
                    ['elephant.png', 'tests/images/multiple/sub/Book 3 - Animals/elephant.png']
                ]
            },
            'tests/images/multiple/Book 1 - Alphabet': {
                'dir': 'Book 1 - Alphabet',
                'src': 'tests/images/multiple/Book 1 - Alphabet',
                'files_list': [
                    ['alphabet_d.png', 'tests/images/multiple/Book 1 - Alphabet/alphabet_d.png'],
                    ['alphabet_b.png', 'tests/images/multiple/Book 1 - Alphabet/alphabet_b.png'],
                    ['alphabet_c.png', 'tests/images/multiple/Book 1 - Alphabet/alphabet_c.png'],
                    ['alphabet_a.png', 'tests/images/multiple/Book 1 - Alphabet/alphabet_a.png']
                ]
            },
            'tests/images/multiple/sub/Book 5 - Alphanimals': {
                'dir': 'Book 5 - Alphanimals',
                'src': 'tests/images/multiple/sub/Book 5 - Alphanimals',
                'files_list': [
                    ['alphabet_d.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/alphabet_d.png'],
                    ['alphabet_b.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/alphabet_b.png'],
                    ['dog.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/dog.png'],
                    ['alphabet_c.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/alphabet_c.png'],
                    ['hummingbird.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/hummingbird.png'],
                    ['monkey.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/monkey.png'],
                    ['dog_cat.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/dog_cat.png'],
                    ['alphabet_a.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/alphabet_a.png'],
                    ['elephant.png', 'tests/images/multiple/sub/Book 5 - Alphanimals/elephant.png']
                ]
            },
            'tests/images/multiple/sub/sub/Book 4 - Alphanumeric': {
                'dir': 'Book 4 - Alphanumeric',
                'src': 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric',
                'files_list': [
                    ['alphabet_d.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/alphabet_d.png'],
                    ['number_6.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_6.png'],
                    ['number_1.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_1.png'],
                    ['alphabet_b.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/alphabet_b.png'],
                    ['number_4.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_4.png'],
                    ['number_3.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_3.png'],
                    ['alphabet_c.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/alphabet_c.png'],
                    ['number_9.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_9.png'],
                    ['number_7.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_7.png'],
                    ['alphabet_a.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/alphabet_a.png'],
                    ['number_2.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_2.png'],
                    ['number_8.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_8.png'],
                    ['number_5.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_5.png'],
                    ['number_10.png', 'tests/images/multiple/sub/sub/Book 4 - Alphanumeric/number_10.png']
                ],
            }
        }
    )
]

generate_filename_data = [
    # "directory" (default) switch
    (
        {'naming_method': 'directory', 'destination': None, 'naming_format': None},
        'cbr', 'some/source/dir', 'book 1',
        TypeError  # destination is None, which should never happen, thus a TypeError
    ),
    (
        {'naming_method': 'directory', 'destination': 'some/destination', 'naming_format': 'should never appear'},
        'cbr', 'some/source/dir/book 1', 'book 1',
        'some/destination/book 1.cbr'
    ),
    # "context" switch
    (
        {'naming_method': 'context', 'destination': None, 'naming_format': None},
        'cbr', 'some/source/dir/book 1', 'book 1',
        TypeError  # destination is None, which should never happen, thus a TypeError
    ),
    (
        {'naming_method': 'context', 'destination': 'some/destination', 'naming_format': None},
        'cbr', 'some/source/dir/book 1', 'book 1',
        'some/destination/book 1.cbr'  # empty naming format equates to using the directory naming method
    ),
    (
        {'naming_method': 'context', 'destination': 'some/destination',
         'naming_format': 'dir:{dir}/src:{src}/ext:{extension}/dest:{destination}'},
        'cbr', 'some/source/dir/book 1', 'book 1',
        'some/destination/dir:book 1/src:some/source/dir/book 1/ext:cbr/dest:some/destination'
    ),
    (
        {'naming_method': 'not supported', 'destination': None, 'naming_format': None},
        'cbr', 'some/source/dir/book 1', 'book 1',
        NotImplementedError
    )
]

unpack_cbz_data = [
    # source_file, destination, expected
    (
        'tests/archive/non-existent',
        None,
        lambda x: isinstance(x, FileNotFoundError),
        None
    ),
    (
        'tests/archives/Book 1 - Alphabet.cbz'.format(OUTPUT_DIR),
        None,
        lambda x: x.startswith('/tmp/tmp'),
        [
            'alphabet_a.png',
            'alphabet_b.png',
            'alphabet_c.png',
            'alphabet_d.png'
        ]
    ),
    (
        'tests/archives/Book 1 - Alphabet.cbz'.format(OUTPUT_DIR),
        '{}/Book 1'.format(OUTPUT_DIR),
        lambda x: x == '{}/Book 1'.format(OUTPUT_DIR),
        [
            'alphabet_a.png',
            'alphabet_b.png',
            'alphabet_c.png',
            'alphabet_d.png'
        ]
    )
]


def get_zip_file_list(filename: str) -> list:
    assert zipfile.is_zipfile(filename)
    with zipfile.ZipFile(filename, 'r') as source_zip:
        assert not source_zip.testzip()
        source_list = source_zip.namelist()
        source_list.sort()
        return source_list
