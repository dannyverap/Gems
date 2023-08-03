from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from gem.model import Gem

class GemClarity(int,Enum):
    SI = 1
    VS = 2
    VVS = 3
    FL = 4

class GemColor(str,Enum):
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"

class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    gem_clarity: Optional[GemClarity] = None
    gem_color: Optional[GemColor] = None

    gem: Optional["Gem"] = Relationship(back_populates="gem_properties")

