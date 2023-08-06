# -*- coding: utf-8 -*-
# @Time: 2022/3/5 13:04
# @File: cmd.py
# @Desc：
import os
import re
import shutil
from os.path import join

from .settings import package_path

name_pattern = '^[a-z0-9\\-]{2,100}$'


class Project:
    def init(self, name: str = "", title: str = "", desc: str = ""):
        """以当前目录为根目录，初始化项目

                Examples:
                    fas project init --title=测试项目 --desc=这是一个测试项目
                Args:
                    name str: 项目名（目录名），如果不传该值，则自动设置为当前目录名
                    title str: 项目标题（显示在交互式文档中）
                    desc str: 项目描述（显示在交互式文档中）
                """
        if len(name) == 0:
            name = os.path.split(os.getcwd())[-1]
        elif re.match(name_pattern, name):
            print("project name check ok")
        else:
            raise Exception(f'project name check error: {name_pattern}')
        project_init(name, title=title, desc=desc)

    def create(self, name: str, title: str = '', desc: str = ''):
        """在当前目录下创建一个目录作为项目根目录，并完成初始化

        Examples:
            fas project create test --title=测试项目 --desc=这是一个测试项目
        Args:
            name str: 项目名（目录名），创建成功之后，会在当前目录下创建一个项目目录
            title str: 项目标题（显示在交互式文档中）
            desc str: 项目描述（显示在交互式文档中）
        """
        if re.match(name_pattern, name):
            print("project name check ok")
        else:
            raise Exception(f'project name check error: {name_pattern}')
        # 创建项目目录，并cd到该目录
        os.mkdir(name)
        os.chdir(name)
        project_init(name, title=title, desc=desc)


def project_init(project_name: str, title: str = '', desc: str = ''):
    """项目初始化
    Args:
        project_name str: 项目名（目录名）
        title str: 项目标题（显示在交互式文档中）
        desc str: 项目描述（显示在交互式文档中）
    """
    if len(title) == 0:
        title = project_name
    else:
        title = title.replace('\n', ' ')

    # vscode, gitignore, Dockerfile
    # cfg = get_config()
    print('parse vscode settings, Dockerfile, readme and gitignore...')
    # os.mkdir(".vscode")
    # shutil.copyfile(join(package_path, 'data', 'vscode_settings.json'),
    #                 join(".vscode", "settings.json"))
    # shutil.copyfile(join(package_path, 'data', 'gitignore'), ".gitignore")
    # shutil.copyfile(join(package_path, 'data', 'Dockerfile'), 'Dockerfile')
    shutil.copyfile(join(package_path, 'data', 'requirements.txt'), 'requirements.txt')
    shutil.copytree(join(package_path, "project", "app"), "app")
    shutil.copytree(join(package_path, "project", "common"), "common")
    shutil.copytree(join(package_path, "project", "core"), "core")
    # init_file('Dockerfile', cfg['author'], cfg['email'])
    # shutil.copyfile(join(package_path, 'data', 'README.md'), 'README.md')
    replaces = {'title': title, 'desc': desc}
    # init_file('README.md', cfg['author'], cfg['email'], replaces=replaces)
    print('--> ok.')


# def create(name: str, title: str = '', desc: str = ''):
#     """在当前目录下创建一个目录作为项目根目录，并完成初始化
#     Examples:
#         fas project create test --title=测试项目 --desc=这是一个测试项目
#     Args:
#         name str: 项目名（目录名），创建成功之后，会在当前目录下创建一个项目目录
#         title str: 项目标题（显示在交互式文档中）
#         desc str: 项目描述（显示在交互式文档中）
#     """
#     if re.match(name_pattern, name):
#         print("project name check ok")
#     else:
#         raise Exception(f'project name check error: {name_pattern}')
#     # 创建项目目录，并cd到该目录
#     os.mkdir(name)
#     os.chdir(name)
#     project_init(name, title=title, desc=desc)


if __name__ == '__main__':
    Project().create("fas")
