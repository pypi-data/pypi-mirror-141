import typing
from datetime import datetime
from http import HTTPStatus
from pydantic import BaseModel, Field


class MessageText(str):
    def contains(self, text: str, case_sens=False) -> bool:
        if not case_sens:
            result = text.lower() in self.lower()
        else:
            result = text in self
        return result

    def contains_any(self, texts: list, case_sens=False) -> bool:
        for text in texts:
            if self.contains(text, case_sens):
                return True
        return False


class Client(BaseModel):
    name: str = Field(...)


class User(BaseModel):
    idx: typing.Union[int, str] = Field(..., example='1')
    username: typing.Optional[str] = Field(None, example='ketovx')
    client: typing.Optional[Client]


class Message(BaseModel):
    user: User = Field(...)
    text: MessageText = Field(...)
    binaries: typing.Optional[str] = Field(None)
    timestamp: typing.Union[float, int] = Field(default=datetime.now().timestamp())

    def __init__(self, *args, **kwargs):
        kwargs['text'] = MessageText(kwargs['text'])
        super().__init__(*args, **kwargs)


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
