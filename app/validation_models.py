import pydantic
from typing import List


class ValidationRequestFieldLogin(pydantic.BaseModel):
    username: str
    password: str


class ValidationRequestFieldRegistration(pydantic.BaseModel):
    username: str
    password: str
    r_password: str

    @pydantic.validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @pydantic.validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class ValidationRequestFieldUnRegistration(pydantic.BaseModel):
    username: str


class ValidationRequestFieldGetNotes(pydantic.BaseModel):
    dashboard_title: str


class ValidationRequestFieldCreateNotes(pydantic.BaseModel):
    dashboard_title: str
    notes: List[str]


class ValidationRequestFieldEditNotes(pydantic.BaseModel):
    note_id: int
    note_new_text: str


class ValidationRequestFieldDeleteNotes(pydantic.BaseModel):
    note_id: int
