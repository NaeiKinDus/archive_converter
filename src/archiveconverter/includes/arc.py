#!/usr/bin/python3
# -*- coding: utf-8 -*

from os import path, rename, mkdir
from tempfile import NamedTemporaryFile, mkdtemp
from typing import Tuple, List, Optional
from zipfile import ZipFile, ZIP_STORED


def create_cbz(files_list: List[Tuple[str, str]], dry_run: bool = False) -> Optional[str]:
    """
    Create a zip containing all the specified files.
    :param files_list: list containing all files to zip
    :type files_list: list
    :param dry_run: set to true to prevent execution and simply output expected commands
    :type dry_run: bool
    :return: zip file path
    :rtype: str
    """
    if dry_run:
        print('create_cbz(): creating a temporary file')
        print('create_cbz(): create a zipfile with compression=ZIP_STORE // compressLevel=7')
    else:
        temp_file = NamedTemporaryFile('xb', delete=False)
        cbz_file = ZipFile(temp_file, mode='w', compression=ZIP_STORED, compresslevel=7)
    for file in files_list:
        if dry_run:
            print('create_cbz(): processing source file "{}", storing as "{}"'.format(file[1], file[0]))
        else:
            cbz_file.write(file[1], arcname=file[0])
    if not dry_run:
        cbz_file.close()
        return temp_file.name
    return None


def unpack_cbz(source_archive: str, destination: Optional[str] = None, dry_run: bool = False) -> Optional[str]:
    """
    Unpacks a CBZ archive to a temporary directory
    :param source_archive: path to archive to be extracted
    :type source_archive: str
    :param destination: directory where the files will be unpacked
    :type destination: str
    :param dry_run: set to true to prevent execution and simply output expected commands
    :type dry_run: bool
    :return:
    """
    if dry_run:
        if destination:
            print('unpack_cbz(): using directory "{}" to unpack'.format(destination))
        else:
            print('unpack_cbz(): creating a temporary directory')
        print('unpack_cbz(): chdir to directory')
        print('unpack_cbz(): unzip source archive "{}"'.format(source_archive))
        return None
    if destination:
        target_dir = destination
    else:
        target_dir = mkdtemp()

    with (ZipFile(source_archive)) as old_archive:
        old_archive.extractall(path=target_dir)

    return target_dir


def create_cbr(files_list: List[Tuple[str, str]], dry_run: bool = False) -> str:
    pass


def unpack_cbr(source_archive: str, destination: Optional[str] = None, dry_run: bool = False) -> Optional[str]:
    pass


class ArchiveHandler:
    """
    Class used to handle (un)archiving operations more easily
    """
    DRY_RUN: bool

    def __init__(self, dry_run: bool = False):
        self.DRY_RUN = dry_run

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
                if self.DRY_RUN:
                    print('ArchiveHandler::unpack_files(): destination does not exist, creating it')
                else:
                    try:
                        mkdir(destination)
                    except Exception:
                        print('Target destination "{}" is not a valid directory'.format(destination))
                        raise
            elif self.DRY_RUN:
                print('ArchiveHandler::unpack_files(): using directory "{}" as repack destination')
        else:
            if self.DRY_RUN:
                print('ArchiveHandler::unpack_files(): creating a temporary directory for repacked files')
            else:
                target_directory = mkdtemp()

        if not archive_type or 'auto' == archive_type:
            extension = archive_file.rsplit('.')[-1]
        else:
            extension = archive_type
        if extension not in self._packers or not self._packers[extension]:
            raise NotImplementedError('No valid unpacking method for extension "{}'.format(extension))
        if self.DRY_RUN:
            print('ArchiveHandler::unpack_files(): files unpacked to target directory')
        else:
            self._packers[extension][1](archive_file, target_directory, self.DRY_RUN)

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
        temp_file = self._packers[extension][0](source_files, self.DRY_RUN)
        if self.DRY_RUN:
            print('ArchiveHandler::pack_files(): moving zip file to "{}"'.format(destination))
        else:
            rename(temp_file, destination)

    """
    Callbacks for different archive types.
    Dictionary of extension pointing to a tuple of packer/unpacker defs.
    """
    _packers = {
        'cbr': (create_cbr, unpack_cbr),
        'cbz': (create_cbz, unpack_cbz)
    }
