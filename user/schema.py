from pydantic import EmailStr, validator
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime


class UserBase(SQLModel):
    username: str
    email: EmailStr
    is_seller: bool = False


class UserCreate(UserBase):
    password: str = Field(max_length=256, min_length=6)
    password_2: str = Field(max_length=256, min_length=6)

    @validator("password_2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v


class UserRead(UserBase):
    id: Optional[int] = Field(primary_key=True, index=True)


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_seller: Optional[bool] = None
    password: Optional[str] = None

