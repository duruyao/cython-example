#!/usr/bin/env python3.7

import os
import re
import sys
import glob
from typing import List

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


# date  : 2022-09-19
# author: duruyao@gmail.com
# usage : python3 setup.py build_ext --cython-c-in-temp -j $(($(nproc) / 2))
# desc  : use cython to compile the python3 sources (in current directory) to shared libraries and executables

def run_cmd(cmd: str, echo=True):
    echo and print(cmd)
    code = os.system(cmd)
    code and exit(code)


def read_cmd_out(cmd: str) -> str:
    return os.popen(cmd).read().replace('\n', '')


def setup_entrances(entrances: List[str], build_dir: str):
    # cython -3 --embed main.py -o main.c
    # gcc -Os $(python3-config --includes) main.c -o main $(python3-config --ldflags --embed)
    for py_path in entrances:
        name = os.path.splitext(os.path.basename(py_path))[0]
        c_dir = os.path.dirname(glob.glob(f'{build_dir}/**/*.c', recursive=True)[0])
        c_path = f'{c_dir}/{name}.c'
        exe_dir = os.path.dirname(glob.glob(f'{build_dir}/**/*.so', recursive=True)[0])
        exe_path = f'{exe_dir}/{name}'
        includes = read_cmd_out('python3-config --includes')
        ldflags = read_cmd_out('python3-config --ldflags') if sys.version_info < (3, 9) \
            else read_cmd_out('python3-config --ldflags --embed')
        cflags = ldflags.split(' -l')[0].replace('-L', '-Wl,-rpath,')
        print(f'building \'{name}\' executable')
        run_cmd(f'cython -3 --embed {py_path} -o {c_path}')
        run_cmd(f'gcc -Os {includes} {c_path} -o {exe_path} {cflags} {ldflags}')


# NOTE: config the re patterns before starting setup
entrance_pattern = r'.*/(main|entrance)\.py'
ignore_pattern = r'.*/(build|compile|setup.*)\.py'

ext_modules = []
entrance_files = []
for py_file in glob.glob(f'{os.getcwd()}/*.py', recursive=False):
    if re.fullmatch(ignore_pattern, py_file):
        pass
    elif re.fullmatch(entrance_pattern, py_file):
        entrance_files.append(py_file)
    else:
        e = Extension(name=os.path.splitext(os.path.basename(py_file))[0], sources=[py_file])
        e.cython_directives = {'language_level': '3'}
        ext_modules.append(e)

setup(
    name='cython-learn',
    version='1.0.0',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

# NOTE: compile the entrance programs after compiling the extensions
setup_entrances(
    entrances=entrance_files,
    build_dir=f'{os.getcwd()}/build'
)
