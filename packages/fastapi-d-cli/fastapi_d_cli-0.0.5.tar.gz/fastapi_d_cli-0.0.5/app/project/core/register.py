# -*- coding: utf-8 -*-
# @Time: 2021/7/2 14:41
# @File: register.py
# @Desc：
import os
import traceback

import redis
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from requests import Request
from starlette.exceptions import HTTPException

from app.common.response_code import response_code
from app.core.config import settings
from app.core.task import Task
from app.core.logger import logger as log
from app.core.scheduler import scheduler


def register_exception(app: FastAPI) -> None:
    """
    注册捕获全局异常
    :param app:
    """

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        log.error(
            f"全局异常\n请求方式：{request.method}\n请求地址：{request.url}\n请求头：Headers:{request.headers}\n错误信息：{traceback.format_exc()}")
        return response_code.parameter_error(msg=exc.errors())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        log.error(
            f"全局异常\n请求方式：{request.method}\n请求地址：{request.url}\n请求头：Headers:{request.headers}\n错误信息：{traceback.format_exc()}")
        if exc.status_code == 401:
            # 验签失败
            return response_code.sign_error(msg=exc.detail)
        elif exc.status_code == 404:
            return response_code.not_found(msg=exc.detail)
        return response_code.server_error()

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        log.error(
            f"全局异常\n请求方式：{request.method}\n请求地址：{request.url}\n请求头：Headers:{request.headers}\n错误信息：{traceback.format_exc()}")
        return response_code.server_error()


def register_redis(app: FastAPI):
    conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    app.state.redis = conn

    @app.on_event("shutdown")
    async def shutdown_redis_event():
        app.state.redis.close()
