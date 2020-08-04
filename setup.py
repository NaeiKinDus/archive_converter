#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from setuptools import setup, find_namespace_packages


setup(
    name="ArchiveConverter",
    version="0.1",
    packages=find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    license="Apache-2",
    description="(re)Packer for comics archives",
    include_package_data=True,
    scripts=[
        "src/archiveconverter/arc_repack.py",
        "src/archiveconverter/img_to_archive.py"
    ]
)
