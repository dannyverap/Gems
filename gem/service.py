from gem.model import Gem
from gem.schema import GemCreate, GemRead, GemWithProperties, GemUpdate
from sqlmodel import select, Session


def service_create(db: Session, gem: GemCreate):
    db_gem = Gem.from_orm(gem)
    db.add(db_gem)
    db.commit()
    db.refresh(db_gem)
    return db_gem  

def service_get_by_id(db:Session,id:int):
    return db.exec(select(Gem).where(Gem.id == id)).first()

def service_update_gem(db:Session, gem: GemUpdate,db_gem:Gem):
    gem_data = gem.dict(exclude_unset=True)
    for key,value in gem_data.items():
        setattr(db_gem, key,value)
    db.add(db_gem)
    db.commit()
    db.refresh(db_gem)
    return db_gem