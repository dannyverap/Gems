from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from schemas.schema import GemClarity, GemColor, GemType


class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    gem_clarity: Optional[GemClarity] = None
    gem_color: Optional[GemColor] = None

