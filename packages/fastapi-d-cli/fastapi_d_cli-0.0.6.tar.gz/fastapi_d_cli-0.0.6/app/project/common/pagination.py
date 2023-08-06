# -*- coding: utf-8 -*- 
# @Time : 2021/5/18 17:11 
# @File : pagination.py
# @Desc : 分页

from __future__ import annotations
import math
from typing import TypeVar, Generic, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from pydantic import BaseModel

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(20, gt=0, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    code: int
    data: dict
    msg: str

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
            cls,
            results: Sequence[T],
            total: int,
            params: Params,
    ) -> Page[T]:
        page = params.page
        size = params.size
        total_pages = math.ceil(total / params.size)
        next = f"?page={page + 1}&size={size}" if (page + 1) <= total_pages else "null"
        previous = f"?page={page - 1}&size={size}" if (page - 1) >= 1 else "null"

        # 此处为了配合API接口返回格式所做处理
        return cls(
            code=200,
            data={"items": results, "total": total, "page": params.page,
                  "size": params.size,
                  "next": next,
                  "previous": previous,
                  "total_pages": total_pages
                  },
            msg="查询成功"
        )
