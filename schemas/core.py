from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, validator
from humps import camel


def to_camel(string):
    return camel.case(string)


class BaseSchema(BaseModel):
    class Config:
        '''
        # キャメルケース　<-> スネークケースの自動変換
        pythonではスネークケースを使用するが、Javascriptではキャメルケースを使用する場合が多いため
        変換する必要がある
        '''
        alias_generator = to_camel 
        allow_population_by_field_name = True


class PagingMeta(BaseSchema):
    current_page: int
    total_page_count: int
    total_data_count: int


class PagingQueryIn(BaseSchema):
    page: int = Query(1)
    per_page: int = Query(30)

    @validator("page")
    def validate_page(cls, v):
        return 1 if not v >= 1 else v

    @validator("per_page")
    def validate_per_page(cls, v):
        return 30 if not v >= 1 else v

    def get_offset(self):
        return (self.page - 1) * self.per_page if self.page >= 1 and self.per_page >= 1 else 0

    def set_paging_query(self, query):
        offset = self.get_offset()
        return query.offset(offset).limit(self.per_page)
