from enum import Enum
from typing import Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from article_playground.types import DictType


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpRequest(BaseModel):
    path: str
    method: HttpMethod
    query: Optional[DictType] = Field(default_factory=dict)
    body: Optional[DictType] = Field(default_factory=dict)
    headers: Optional[DictType] = Field(default_factory=dict)

__all__= ["notion", "client"]
