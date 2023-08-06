# -*- coding: utf-8 -*-
# @Time: 2021/7/10 14:49
# @File: response_code.py
# @Desc：响应格式

__all__ = ["response_code"]

from typing import Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from starlette import status
from pydantic.generics import GenericModel
from typing import Generic, TypeVar

T = TypeVar('T')  # 泛型类型 T


class RestfulModel(GenericModel, Generic[T]):
    code: int
    msg: str
    data: T


class ResponseCode(object):

    @staticmethod
    def response(*, status_code: int = 200, code: int, data: Union[list, dict, str] = None, msg: str = "") -> Response:
        return JSONResponse(
            status_code=status_code,
            content={
                "code": code,
                "msg": msg,
                "data": jsonable_encoder(data)
            })

    @staticmethod
    def success(*, data: Union[list, dict, str], msg: str = "请求成功") -> RestfulModel:
        return RestfulModel(
            code=200,
            data=data,
            msg=msg
        )

    @staticmethod
    def do_success(*, data: Union[list, dict, str], msg: str = "操作成功") -> RestfulModel:
        return RestfulModel(
            code=200,
            data=data,
            msg=msg
        )

    def not_found(self, *, msg: str = "Not Found") -> Response:
        return self.response(
            status_code=status.HTTP_404_NOT_FOUND,
            code=404,
            msg=msg
        )

    def server_error(self, *, msg: str = "系统异常，请稍后再试") -> Response:
        return self.response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=5003,
            msg=msg
        )

    def failed(self, *, msg: str = "请求失败") -> Response:
        return self.response(
            code=4001,
            msg=msg
        )

    def do_failed(self, *, msg: str = "操作失败") -> Response:
        return self.response(
            code=4002,
            msg=msg
        )

    def parameter_error(self, *, msg: str = "参数错误") -> Response:
        return self.response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code=4003,
            msg=msg
        )

    def system_error(self, *, msg: str = "系统错误") -> Response:
        return self.response(
            code=4004,
            msg=msg
        )

    def sign_error(self, *, msg: str = "验签失败") -> Response:
        return self.response(
            code=4005,
            msg=msg
        )

    def user_not_exists(self, *, msg: str = "用户不存在") -> Response:
        return self.response(
            code=4006,
            msg=msg
        )

    def uid_invalid(self, *, msg: str = "无效用户") -> Response:
        """
        无效用户返回格式
        :param msg:
        :return:
        """
        return self.response(
            code=4007,
            msg=msg
        )

    def key_error(self, *, msg: str = "无效key") -> Response:
        return self.response(
            code=4008,
            msg=msg
        )

    def ext_error(self, *, msg: str = "只能上传图片") -> Response:
        return self.response(
            code=4009,
            msg=msg
        )

    def size_error(self, *, msg: str = "文件大小限制") -> Response:
        return self.response(
            code=4010,
            msg=msg
        )

    def account_disabled(self, *, msg: str = "账号被限制") -> Response:
        return self.response(
            code=4011,
            msg=msg
        )

    def uid_error(self, *, msg: str = "用户ID不正确") -> Response:
        return self.response(
            code=4012,
            msg=msg
        )

    def ws_close(self, *, msg: str = "连接已断开") -> Response:
        return self.response(
            code=4013,
            msg=msg
        )

    def none_edit(self, *, msg: str = "没有数据被修改") -> Response:
        return self.response(
            code=4014,
            msg=msg
        )

    def send_success(self, *, msg: str = "消息发送成功") -> Response:
        return self.response(
            code=200,
            msg=msg
        )

    def too_many_attempts(self, *, msg: str = "请求太快了，请稍后再试") -> Response:
        return self.response(
            code=429,
            msg=msg
        )


response_code = ResponseCode()
