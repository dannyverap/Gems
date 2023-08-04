from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    username: str = Field (index= True)
    password: str = Field(max_length=256,min_length=6)
    email: str
    created_at: datetime = datetime.now()
    is_seller: bool = False
