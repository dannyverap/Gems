from gem_properties.model import GemProperties
from gem_properties.schema import GemPropertiesCreate, GemPropertiesUpdate
from sqlmodel import select, Session


def service_create(db: Session, gem_properties: GemPropertiesCreate):
    db_gem_properties  = GemProperties.from_orm(gem_properties)
    db.add(db_gem_properties )
    db.commit()
    db.refresh(db_gem_properties )
    return db_gem_properties   

def service_get_gem_properties(db: Session, offset: int, limit: int):
    return db.query(GemProperties).offset(offset).limit(limit).all()

def service_get_by_id(db:Session,id:int):
    return db.exec(select(GemProperties).where(GemProperties.id == id)).first()

def service_update_gem_properties(db:Session, gem_properties: GemPropertiesUpdate,db_gem_properties :GemProperties):
    gem_properties_data = gem_properties.dict(exclude_unset=True)
    for key,value in gem_properties_data.items():
        setattr(db_gem_properties , key,value)
    db.add(db_gem_properties)
    db.commit()
    db.refresh(db_gem_properties )
    return db_gem_properties 

def service_delete(db:Session, db_gem_properties :GemProperties):
    db.delete(db_gem_properties)
    db.commit()
    return "Deleted :("