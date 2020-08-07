#!/usr/bin/python3
# -*- coding: utf-8 -*

from os import path, rename, mkdir
from tempfile import NamedTemporaryFile, mkdtemp, gettempdir
from typing import Tuple, List, Optional
from uuid import uuid4
from zipfile import ZipFile, ZIP_STORED

from archiveconverter.includes.common import run_command
from . import RAR_BIN


RAR_FILES_STEP = 50


def create_cbz(files_list: List[Tuple[str, str]]) -> Optional[str]:
    """
    Create a zip containing all the specified files.
    :param files_list: list containing all files to zip
    :type files_list: list
    :return: zip file path
    :rtype: str
    """
    temp_file = NamedTemporaryFile('xb', delete=False)
    filename = temp_file.name
    cbz_file = ZipFile(temp_file, mode='w', compression=ZIP_STORED, compresslevel=7)
    for file in files_list:
        cbz_file.write(file[1], arcname=file[0])
    cbz_file.close()
    temp_file.close()
    return filename


def unpack_cbz(source_archive: str, destination: Optional[str] = None) -> Optional[str]:
    """
    Unpacks a CBZ archive to a temporary directory
    :param source_archive: path to archive to be extracted
    :type source_archive: str
    :param destination: directory where the files will be unpacked
    :type destination: str
    :return: returns the directory where files were unarchived
    :rtype: Optional[str]
    """
    if destination:
        target_dir = destination
    else:
        target_dir = mkdtemp()

    with (ZipFile(source_archive)) as old_archive:
        old_archive.extractall(path=target_dir)

    return target_dir


def create_cbr(files_list: List[Tuple[str, str]]) -> Optional[str]:
    """
    Create a CBR archive
    :param files_list: list of files to add to the archive
    :type files_list: List[Tuple[str, str]]
    :return: returns the path to the created archive file (or None if dry-run)
    :rtype: Optional[str]
    """
    # RAR_BIN 'a -m<0=store,...5=best> -ma<archiving_version> <archive_name> files...'
    if not RAR_BIN:
        raise RuntimeError('Binary "rar" was not found, please install it and ensure it is in your PATH variable')
    command = [RAR_BIN, 'a', '-m0', '-ma4']
    filename = path.join(gettempdir(), '{}.cbr'.format(uuid4()))
    files_list = list(map(lambda x: x[1], files_list))
    sublists = [files_list[pos:pos+RAR_FILES_STEP] for pos in range(0, len(files_list), RAR_FILES_STEP)]
    for call_iter in sublists:
        run_command(command + [filename] + call_iter)
    return filename


def unpack_cbr(source_archive: str, destination: Optional[str] = None) -> Optional[str]:
    """
    Unpacks a CBR archive to a temporary directory
    :param source_archive: path to archive to be extracted
    :type source_archive: str
    :param destination: directory where the files will be unpacked
    :type destination: str
    :return: returns the directory where files were unarchived
    :rtype: Optional[str]
    """
    if not RAR_BIN:
        raise RuntimeError('Binary "rar" was not found, please install it and ensure it is in your PATH variable')
    if not path.isfile(source_archive):
        raise FileNotFoundError('"{}" is not a valid archive file'.format(source_archive))
    if destination:
        destination = destination.rstrip(path.sep)
        if not path.isdir(destination):
            mkdir(destination)
        target_dir = destination
    else:
        target_dir = mkdtemp()
    command = [RAR_BIN, 'e', '-o+', source_archive, target_dir]
    run_command(command)
    return target_dir


class ArchiveHandler:
    """
    Class used to handle (un)archiving operations more easily
    """
    def unpack_archive(
            self, archive_file: str, destination: Optional[str] = None, archive_type: Optional[str] = 'auto'
    ) -> str:
        """
        Unpack archive
        :param archive_file: archive to be processed
        :type archive_file: str
        :param destination: directory where files will be unpacked; if empty, use a temp directory
        :type destination: str
        :param archive_type: type of archive that will be unpacked; use auto to determine type using extension.
        :type archive_type: str
        :return: directory where the files were unpacked
        :rtype: str
        """
        target_directory = ''
        if destination:
            target_directory = destination
            if not path.isdir(destination):
                try:
                    mkdir(destination)
                except Exception:
                    print('Target destination "{}" is not a valid directory'.format(destination))
                    raise
        else:
            target_directory = mkdtemp()

        if not archive_type or 'auto' == archive_type:
            extension = archive_file.rsplit('.')[-1]
        else:
            extension = archive_type
        if extension not in self._packers or not self._packers[extension]:
            raise NotImplementedError('No valid unpacking method for extension "{}'.format(extension))
        self._packers[extension][1](archive_file, target_directory)
        return target_directory

    def pack_files(
            self, source_files: List[Tuple[str, str]], destination: str, archive_type: Optional[str] = 'auto'
    ) -> None:
        """
            Unpack archive
            :param source_files: a list of tuples containing the filename and the filepath.
            :type source_files: list
            :param destination: directory where the archive will be stored
            :type destination: str
            :param archive_type: type of archive to be archived; use auto to determine type using destination extension.
            :type archive_type: str
            :return: archive file generated
            :rtype: str
            """
        if 'auto' == archive_type:
            extension = destination.rsplit('.')[-1]
        else:
            extension = archive_type
        if extension not in self._packers or not self._packers[extension]:
            raise NotImplementedError('No valid unpacking method for extension "{}'.format(extension))
        temp_file = self._packers[extension][0](source_files)
        rename(temp_file, destination)

    """
    Callbacks for different archive types.
    Dictionary of extension pointing to a tuple of packer/unpacker defs.
    """
    _packers = {
        'cbr': (create_cbr, unpack_cbr),
        'cbz': (create_cbz, unpack_cbz)
    }
