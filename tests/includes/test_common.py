# Tests includes/common.py
from pytest import mark


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
        }
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


@mark.parametrize("test_dir,expected", get_files_data)
def test_get_files(test_dir: str, expected: dict):
    from archiveconverter.includes.common import get_files
    found_files = get_files(test_dir)
    assert expected == found_files


@mark.parametrize("cli_args,extension,source,cont_dir,expected", generate_filename_data)
def test_generate_filename(cli_args, extension, source, cont_dir, expected):
    from archiveconverter.includes.common import generate_filename
    try:
        generated = generate_filename(cli_args, extension, source, cont_dir)
    except Exception as e:
        assert isinstance(e, expected)
    else:
        assert generated == expected


def test_run_command():
    pass
