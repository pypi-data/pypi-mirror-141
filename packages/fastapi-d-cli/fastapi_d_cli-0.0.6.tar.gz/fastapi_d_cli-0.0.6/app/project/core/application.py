# -*- coding: utf-8 -*- 
# @Time : 2021/6/15 14:23 
# @File : application.py
# @Desc :
import os

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.core import log
from app.business_api.controller import api_router as business_api_router
from app.core.config import settings
from app.core.register import register_exception, register_redis
from app.core.scheduler import scheduler, my_listener
from app.sentry_api.controller import sentry_api_router
from app.scheduler_api.controller import api_router as scheduler_api_router


def create_app():
    """
    创建应用程序
    :return: 主应用程序
    """
    app = FastAPI()
    log.info("应用程序启动成功")
    # 挂载image文件夹
    app.mount("/image", StaticFiles(directory=os.path.join(settings.BASE_APP_DIR, "image")), name="image")

    # 挂载子应用
    business = business_app(app)
    sentry = sentry_app(app)

    # 注册全局捕获异常
    register_exception(app)
    register_exception(business)
    register_exception(sentry)
    # 注册Redis
    register_redis(business)

    return app


def business_app(main: FastAPI):
    """
    业务子应用
    :param main: 主应用
    :return: 子应用
    """
    # 业务应用
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(business_api_router, )
    # 挂载到主应用
    main.mount("/business", app)
    log.info("子应用【business】挂载成功")
    add_pagination(app)
    return app


def sentry_app(main: FastAPI):
    """
    业务子应用
    :param main: 主应用
    :return: 子应用
    """
    # 业务应用
    app = FastAPI()
    app.include_router(sentry_api_router, )
    # 挂载到主应用
    main.mount("/sentry", app)
    log.info("子应用【sentry】挂载成功")
    add_pagination(app)
    return app
