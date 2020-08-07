# -*- coding: utf-8 -*-

from natsort import natsorted, ns
import os
from subprocess import check_call, Popen, PIPE
from typing import List, Dict, Optional, Union, Tuple
from unicodedata import normalize


format_parameters = {
    'dir': 'Directory containing the image files',
    'src': 'directory where the file resides',
}

supported_naming_methods = {
    'context': 'use context variables (see format parameters)',
    'directory': 'use the name of the parent directory (`dir`)'
    # The following are not yet implemented
    #'match-path': 'use a matching template against `dir`',
    #'match-file': 'use a matching template against a filename'
}

allowed_file_extensions = [
    'jpg', 'jpeg', 'png', 'bmp', 'art', 'gif', 'pm', 'ppm', 'tif', 'tiff'
]

allowed_archive_extensions = [
    'cbr', 'cbz'
]


def get_files(source: str, file_types: Optional[List] = None, files_list: Optional[Dict] = None, sort_list: bool = True) -> Dict:
    """
    Retrieves a list of directories and images recursively.

    :param source: directory to scan
    :type source: str
    :param file_types: list of allowed extensions
    :type file_types: list
    :param files_list: processed files
    :type files_list: dict
    :return: a dictionary containing all matching files and meta information
    :rtype: dict
    """
    s_source = source.rstrip(os.path.sep)
    if not files_list:
        files_list = {}

    for file in os.scandir(s_source):
        if file.is_dir():
            files_list = get_files(os.path.join(s_source, file.name), file_types, files_list, False)
            continue
        filepath = os.path.join(s_source, file.name)
        extension = file.name.split('.')[-1].lower()

        if file_types and extension not in file_types:
            continue

        if s_source not in files_list:
            files_list[s_source] = {
                'dir': os.path.split(s_source)[-1],
                'src': s_source,
                'files_list': []
            }
        files_list[s_source]['files_list'].append((file.name, filepath))

    if sort_list:
        for item_name, item_data in files_list.items():
            item_data['files_list'] = natsorted(item_data['files_list'], alg=ns.IGNORECASE)
    return files_list


def generate_filename(cli_arguments: dict, extension: str, source: str, cont_dir: str) -> str:
    """
    Generate a name for the CBZ file using one of various ways.
    :param cli_arguments: parsed CLI arguments
    :type cli_arguments: dict
    :param extension: extension of the generated archive
    :type extension: str
    :param source: source directory of the images
    :type source: str
    :param cont_dir: directory containing the images
    :type cont_dir: str
    :return: a filename including extension matching the formatting rule.
    :rtype: str
    """

    context = {key: None for key in format_parameters.keys()}
    context['dir'] = cont_dir
    context['src'] = source
    context['extension'] = extension

    context['destination'] = cli_arguments.get('destination')
    naming_format = cli_arguments.get('naming_format', '') or ''

    naming_method = cli_arguments.get('naming_method')
    if not naming_method or naming_method not in supported_naming_methods.keys():
        raise NotImplementedError('Error: "{}" is not a valid naming method'.format(naming_method))
    if 'directory' == naming_method or not naming_format:
        return os.path.join(context['destination'], '{}.{}'.format(cont_dir, extension))
    elif 'context' == naming_method:
        return os.path.join(context['destination'], naming_format.format_map(context))
    raise NotImplementedError('Error: "{}" is not available'.format(naming_method))


def run_command(command: Union[str, list], verbose: bool = False) -> Tuple[int, str]:
    """
    Executes a command
    :param command: command to be executed; may be an str or a list
    :type command: Union[str, list]
    :param verbose: whether to capture the command output
    :type verbose: bool
    :return: a tuple with the return code and a string, empty if verbose is not True
    :rtype: Tuple[int, str]
    """
    if isinstance(command, str):
        command_list = command.split()
    else:
        command_list = command
    if verbose:
        proc = Popen(command_list, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate()
        return proc.returncode, output.decode('utf-8')

    with open(os.devnull, 'w') as devnull:
        return (
            check_call(
                command_list,
                stdin=devnull,
                stdout=devnull,
                stderr=devnull
            ),
            ''
        )


def strip_accents(filename: str) -> str:
    return normalize('NFKD', filename).encode('ASCII', 'ignore').decode('utf-8')
