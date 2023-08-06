# -*- coding: utf-8 -*- 
# @Time : 2021/6/15 10:27 
# @File : __init__.py.py
# @Desc :
from fastapi import APIRouter

api_router = APIRouter(prefix="/v1")
api_router.include_router(user_router)
