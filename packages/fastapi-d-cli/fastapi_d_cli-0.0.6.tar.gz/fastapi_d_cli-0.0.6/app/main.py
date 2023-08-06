# -*- coding: utf-8 -*-
# @Time: 2022/3/9 16:21
# @File: main.py
# @Desc：
import fire

from .cmd import project
from .settings import VERSION


def version() -> str:
    """版本号"""
    return f"Version: {VERSION}"


def main():
    """主入口"""
    fire.Fire({
        'version': version,
        'project': project()
    })


if __name__ == '__main__':
    main()
