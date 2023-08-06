# -*- coding: utf-8 -*- 
# @Time : 2021/6/15 10:32 
# @File : __init__.py.py
# @Desc : 数据模式
from typing import Optional

from pydantic import BaseModel


class BaseSchemasModel(BaseModel):
    device: Optional[str] = None
    version: Optional[str] = None
    idcode: Optional[str] = None
