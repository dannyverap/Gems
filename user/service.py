from user.model import *
from user.schema import UserCreate, UserUpdate
from sqlmodel import select, Session


def service_create(db: Session, user: UserCreate):
    db_user = User.from_orm(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  

def service_get_users(db: Session, offset: int, limit: int):
    return db.query(User).offset(offset).limit(limit).all()

def service_get_by_id(db:Session,id:int):
    return db.exec(select(User).where(User.id == id)).first()

def service_update_user(db:Session, user: UserUpdate,db_user:User):
    user_data = user.dict(exclude_unset=True)
    for key,value in user_data.items():
        setattr(db_user, key,value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def service_delete(db:Session, db_user:User):
    db.delete(db_user)
    db.commit()
    return "Deleted :("