# -*- coding: utf-8 -*-
# @Time: 2022/3/9 16:31
# @File: setup.py
# @Desc：

import os
from distutils.core import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), encoding='utf8') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("VERSION"):
            # VERSION = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


LONG_DESCRIPTION = """
使用：

- 完整命令：fas-cli
""".strip()

SHORT_DESCRIPTION = """FastAPI脚手架""".strip()

DEPENDENCIES = [
    'fire',
]
VERSION = get_version("app/settings.py")
URL = 'http://bitbucket.org/tarek/distribute/issues/'
setup(
    name='fastapi_d_cli',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Desire',
    author_email='',
    license='Apache Software License',

    keywords='fastapi',
    packages=['fastapi_cli'],
    package_dir={'fastapi_cli': 'app'},
    package_data={'fastapi_cli': [
        os.path.join('data', '*'),
        os.path.join('project', '*'),
        os.path.join('project', 'app', '*'),
        os.path.join('project', 'common', '*'),
        os.path.join('project', 'core', '*'),
        os.path.join('project', 'static', '*'),
        os.path.join('project/app', 'controller', '*'),
        os.path.join('project/app', 'models', '*'),
        os.path.join('project/app', 'schemas', '*'),
        os.path.join('project/app', 'service', '*'),
        os.path.join('project/core', 'config', '*'),
    ]},
    entry_points={  # 安装命令
        "console_scripts": [
            "fas-cli=fastapi_cli.main:main",
            # 命令别名
            # "=fastapi_start.main:main",
        ],
    },
    python_requires=">=3.6",
)
