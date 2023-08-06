# -*- coding: utf-8 -*-
# @Time: 2021/7/21 11:34
# @File: security.py
# @Desc：
from datetime import timedelta, datetime
from typing import Optional
from jose import jwt
from fastapi import Header, HTTPException
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from app.common.response_code import response_code
from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码验证
    :param plain_password: 原密码
    :param hashed_password: 加密后的密码
    :return: Bool
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """
    密码加密
    :param password: 待加密的密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建令牌
    :param data: 需要进行JWT令牌加密的数据（解密的时候会用到）
    :param expires_delta: 令牌有效期
    :return: token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    # 添加失效时间
    to_encode.update({"exp": expire})
    # SECRET_KEY：密钥
    # ALGORITHM：JWT令牌签名算法
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def check_jwt_token(token: Optional[str] = Header(None)):
    """
    验证token
    :param token:
    :return: 返回用户信息
    """
    try:
        if token:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            id: str = payload.get("sub")
            # 通过解析得到的username,获取用户信息,并返回
            return id
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is None"
        )
    except (jwt.JWTError, jwt.ExpiredSignatureError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Error"
        )


if __name__ == '__main__':
    import asyncio

    result = asyncio.run(get_password_hash("jw@9988"))
    print(result)
