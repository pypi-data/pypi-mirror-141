# -*- coding: utf-8 -*-
# @Time: 2022/1/21 16:12
# @File: __init__.py
# @Desc：
import os

from app.core.config.config import settings

# 添加项目根路径配置
settings.__setattr__("BASE_APP_DIR", os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
