#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging

import numpy as np
import pandas as pd
from xenoslib.base import ArgMethodBase

# Set file path as current path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)


def init_log():
    """set logging"""
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s %(levelname)s [line:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logfile = logging.FileHandler(f'{os.path.splitext(__file__)[0]}.log')
    logfile.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[logfile, console])


class Dockerfile:
    images = [
        'python:3.6-alpine',
        'python:3.7-alpine',
        'python:3.8-alpine',
        'python:3.9-alpine',
        'python:3.10-alpine',
        'python:3.11-rc-alpine',
        'python:3.6-slim',
        'python:3.7-slim',
        'python:3.8-slim',
        'python:3.9-slim',
        'python:3.10-slim',
        'python:3.11-rc-slim',
    ]
    base_type = None

    image = 'python:3.8.13-alpine3.15'

    def __init__(self, image, libs=None):
        self.image = image
        if 'alpine' in image:
            self.base_type = 'alpine'
        elif 'slim' in image:
            self.base_type = 'debian'
        self.libs = libs
        if libs is None:
            self.libs = self.read_libs()
            self.libs.discard('')
        print(self.libs)

    def read_libs(self):
        with open('item/requirements.txt') as r:
            return {line.strip() for line in r.readlines()}

    def generate(self, compact=False):
        lines = ['FROM ' + self.image, *self.get_lines(compact=compact), '']
        return '\n'.join(lines)

    def get_lines(self, compact=True):
        if compact:
            yield 'RUN ' + ' &&\\\n    '.join(self.get_cmds())
        else:
            for cmd in self.get_cmds():
                yield f'RUN {cmd}'

    def get_cmds(self):
        yield from self.get_deps_cmds()
        yield from self.get_pip_cmds()

    def get_pip_cmds(self):
        yield 'pip3 install --no-cache-dir pip --upgrade'
        for lib in self.libs:
            if '>' in lib or '<' in lib:
                lib = f'"{lib}"'
            yield f'pip3 install --no-cache-dir {lib}'

    def get_deps_cmds(self):
        deps = self.get_deps()
        if not deps:
            return
        if self.base_type == 'debian':
            yield 'apt update'
            for dep in deps:
                yield f'apt install -y {dep}'
        elif self.base_type == 'alpine':
            for dep in deps:
                yield f'apk add --no-cache {dep}'

    def get_deps(self):
        all_deps = set()
        df = pd.read_csv('data.csv', index_col='lib')
        df = df.loc[:, df.columns.isin([self.base_type, self.image])]  # 筛选符合条件的列
        for lib in self.libs:
            deps = df[[lib.lower().startswith(x.lower()) for x in df.index]]
            deps = set(deps.values.reshape(-1).tolist())
            deps.discard(np.nan)
            deps = ' '.join(deps)
            all_deps |= set(deps.split(' '))
        return all_deps

    def export(self, compact=False):
        with open('Dockerfile', 'w') as w:
            w.write(self.generate(compact))

    def validate(self):
        os.system('cat Dockerfile')
        return os.system('docker build .') == 0


def main():
    Dockerfile().export()


class ArgMethod(ArgMethodBase):
    """onedrive tenant util"""

    @staticmethod
    def validate(image, lib='', compact=False):
        libs = [lib] if lib else None
        df = Dockerfile(image, libs=libs)
        df.export(compact)
        return df.validate()

    @staticmethod
    def export(image, lib='', compact=False):
        libs = [lib] if lib else None
        df = Dockerfile(image, libs=libs)
        return df.export(compact)

    @staticmethod
    def test():
        libs = [
            'requests',
            'cffi',
        ]
        image = 'python:3.11-rc-slim'
        # dfx = Dockerfile(image, libs)
        dfx = Dockerfile(image)
        # print(dfx.get_deps())
        print(dfx.export())
        # print(dfx.read_libs())
        return

    def test2():
        df = pd.read_csv('data.csv')
        lib = 'numpy==1.17.3'
        datas = df[[lib.startswith(x) for x in df.lib]][['alpine', 'python:3.10-alpine']]
        
        # row = df[lib.str.startswith]
        print(set(datas.values.reshape(-1).tolist()))

        # df.loc[]
        # for i in row.get('alpine').values:
            # print(i.empty)
        # print(row.get('alpine').values[0])
        # print(row.get('alpine').values[1])
            # df = pd.read_csv('data.csv')
            # row = df[[lib.lower().startswith(x.lower()) for x in df.lib]]
            # for item in (self.base_type, self.image):
                # if row.get(item) is not None and not row.get(item).empty:
                    # for deps in row.get(item).values:
                        # if isinstance(deps, str):
                            # all_deps |= set(deps.split(' '))
        
        return


if __name__ == '__main__':
    # init_log()
    ArgMethod()
    # ArgMethod.test2()
    # ArgMethod.export('python:3.10-alpine')
