from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from gem.model import Gem


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    username: str = Field (index= True)
    password: str = Field(max_length=256,min_length=6)
    email: str= Field (index= True)
    created_at: datetime = datetime.now()
    is_seller: bool = False

    gems: Optional["Gem"] = Relationship(back_populates="seller")
