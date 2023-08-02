from sqlmodel import SQLModel, Field, Relationship
from typing import Optional,TYPE_CHECKING
from gem_tipes.schema import GemType
if TYPE_CHECKING:
    from gem_properties.model import GemProperties



class Gem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    price: float
    available: bool = True
    gem_types: GemType = GemType.EMERALD

    gem_properties_id: Optional[int] = Field(foreign_key="gemproperties.id", default=None)
    gem_properties: Optional["GemProperties"] = Relationship(back_populates="gem")


