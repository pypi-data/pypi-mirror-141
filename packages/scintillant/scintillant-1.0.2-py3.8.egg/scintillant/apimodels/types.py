import typing
from datetime import datetime
from http import HTTPStatus
from pydantic import BaseModel, Field


class Client(BaseModel):
    name: str = Field(...)


class User(BaseModel):
    idx: typing.Union[int, str] = Field(..., example='1')
    username: typing.Optional[str] = Field(None, example='ketovx')
    client: typing.Optional[Client]


class Message(BaseModel):
    user: User = Field(...)
    text: str = Field(...)
    binaries: typing.Optional[str] = Field(None)
    timestamp: typing.Union[float, int] = Field(default=datetime.now().timestamp())


class SkillResponse(BaseModel):
    """ Response Model for testsuite
    """
    status: HTTPStatus = Field(..., example=HTTPStatus.OK)
    text: typing.Optional[str] = Field(None, example='Any text...')
    binaries: typing.Optional[str] = Field(None)
    context: typing.Optional[dict] = Field(None)


class SkillRequest(BaseModel):
    """ Request model for testsuite
    """
    message: Message
    context: dict = Field({})
