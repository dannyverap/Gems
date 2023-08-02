from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from gem_tipes.schema import GemClarity, GemColor

if TYPE_CHECKING:
    from gem.model import Gem


class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    gem_clarity: Optional[GemClarity] = None
    gem_color: Optional[GemColor] = None

    gem: Optional["Gem"] = Relationship(back_populates="gem_properties")

