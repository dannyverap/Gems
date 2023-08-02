from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from gem_tipes.schema import GemClarity, GemColor


class GemPropertiesBase(SQLModel):
    size: float = 1
    gem_clarity: Optional[GemClarity] = None
    gem_color: Optional[GemColor] = None

class GemPropertiesCreate(GemPropertiesBase):
    pass 

class GemPropertiesRead(GemPropertiesBase):
    id: Optional[int] = Field(primary_key=True)

class GemPropertiesUpdate(SQLModel):
    size: Optional[float]=1
    gem_clarity: Optional[GemClarity] = None
    gem_color: Optional[GemColor] = None

