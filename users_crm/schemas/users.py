from datetime import datetime, timezone
from typing import Annotated, Literal, Optional

from pydantic import AfterValidator, BaseModel, BeforeValidator, EmailStr, Field, SecretStr

PyObjectId = Annotated[str, BeforeValidator(str), AfterValidator(str)]


class UserBaseSchema(BaseModel, populate_by_name=True):
    first_name: str = Field(...)
    last_name: Optional[str] = Field('')


class UserSchemaAddInput(UserBaseSchema):
    password: str = SecretStr(...)
    email: EmailStr = Field(...)


class UserSchemaAddDb(UserBaseSchema):
    role: Literal['admin', 'dev', 'simple mortal'] = Field(default='simple mortal')
    password: str = SecretStr(...)
    email: EmailStr = Field(...)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class UserSchemaUpdate(UserBaseSchema):
    role: Literal['admin', 'dev', 'simple mortal'] = Field(default='simple mortal')
    is_active: bool = Field(default=True)


class UserSchema(UserBaseSchema):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    role: Literal['admin', 'dev', 'simple mortal'] = Field(default='simple mortal')
    is_active: bool = Field(default=True)
    email: EmailStr = Field(...)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    last_login: Optional[datetime] = Field(default=None)


class UserCreatedMsgSchema(BaseModel, populate_by_name=True):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    created_at: datetime = Field(...)
