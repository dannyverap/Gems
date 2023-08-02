from sqlmodel import SQLModel, Field
from typing import Optional, List
from gem_tipes.schema import GemType
from gem_properties.schema import GemPropertiesRead


class GemBase(SQLModel):
    price: float
    available: bool = True
    gem_types: GemType = GemType.EMERALD


class GemCreate(GemBase):
    gem_properties_id: Optional[int] = Field(
        foreign_key="gemproperties.id", default=None
    )


class GemRead(GemBase):
    id: Optional[int] = Field(primary_key=True)


class GemUpdate(SQLModel):
    price: Optional[float] = None
    available: Optional[bool] = True
    gem_types: Optional[GemType] = GemType.EMERALD
    gem_properties_id: Optional[int] = Field(
        foreign_key="gemproperties.id", default=None
    )


class GemWithProperties(GemRead):
    gem_properties: Optional[List[GemPropertiesRead]] = None
