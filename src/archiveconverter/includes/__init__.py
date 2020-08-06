# -*- coding: utf-8 -*-

RAR_BIN = None
try:
    from distutils import spawn
    RAR_BIN = spawn.find_executable('rar')
except:
    pass

if not RAR_BIN:
    try:
        from shutil import which
        RAR_BIN = which('rar')
    except:
        pass
