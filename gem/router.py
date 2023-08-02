from fastapi import APIRouter, status, Depends, HTTPException, Query,responses
from sqlmodel import Session
from gem.schema import GemCreate, GemRead, GemUpdate, GemWithProperties
from typing import List
from gem.service import *
from dependencies import get_db

gem_router = APIRouter()


@gem_router.get("/")
def hello():
    return "Hello World! 2"

@gem_router.post("/", response_model=GemRead,status_code=status.HTTP_201_CREATED)
def create_gem(*,db:Session = Depends(get_db), gem:GemCreate):
    new_gem = service_create(db, gem)
    return new_gem

@gem_router.get("/all", response_model=List[GemWithProperties], status_code=status.HTTP_200_OK)
def get_gems(
    *,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    gems = service_get_gems(db, offset, limit)
    return gems

@gem_router.get("/{gem_id}", response_model=GemWithProperties, status_code=status.HTTP_200_OK)
def get_gem_by_id(*,db: Session = Depends(get_db) ,gem_id:int):
    gem = service_get_by_id(db, id=gem_id)
    if not gem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gem not found")
    return gem

@gem_router.patch("/{gem_id}", response_model=GemWithProperties,status_code=status.HTTP_200_OK)
def update_gem(*,db:Session=Depends(get_db), gem_id:int, gem:GemUpdate):
    db_gem = service_get_by_id(db,id=gem_id)
    if not db_gem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gem not found")
    
    updated_gem = service_update_gem(db,gem,db_gem)
    return updated_gem

@gem_router.delete("/{gem_id}", status_code=status.HTTP_200_OK)
def delete_gem(*,db:Session=Depends(get_db), gem_id:int):
    db_gem = service_get_by_id(db,id=gem_id)
    if not db_gem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gem not found")
    return service_delete(db,db_gem)

# @gem_router.post("/",response_model=GemRead,status_code=status.HTTP_201_CREATED)
# def create_gem(*, session: Session = Depends(get_session), gem:GemCreate):
#     check_mail=session.exec(select(Gem).where(gem.mail == gem.mail)).first()
#     if check_mail is not None:
#         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email already in use")
#     gem.password = get_password_hash(gem.password)
#     db_gem = gem.from_orm(gem)
    
#     session.add(db_gem)
#     session.commit()
#     session.refresh(db_gem)
#     return db_gem

# @gem_router.get("/all", response_model=List[GemWithProperties],status_code=status.HTTP_200_OK)
# def get_all_gems(
#    *, 
#     session: Session = Depends(get_session),
#     offset: int = 0,
#     limit: int = Query(default=100, lte=100),
#     ):
#     gems = session.exec(select(Gem).offset(offset).limit(limit)).all()
#     return gems

# @gem_router.get("/{gem_id}",response_model=GemWithProperties, status_code=status.HTTP_200_OK)
# def get_gem_by_id(*,session: Session = Depends(get_session), gem_id:int):
#     gem = session.exec(select(Gem).where(gem.id == gem_id)).first()
#     if not gem:
#         raise HTTPException(status_code=404, detail="gem not found")
#     return gem


# @gem_router.patch("/{gem_id}",response_model=GemRead, status_code = status.HTTP_200_OK)
# def update_gem(*,session: Session = Depends(get_session),gem_id:int, gem:GemUpdate):
    
#     db_gem = session.get(gem, gem_id)
#     if not db_gem:
#         raise HTTPException(status_code=404
#         , detail="gem not found")
    
#     gem_data = gem.dict(exclude_unset=True)
#     for key,value in gem_data.items():
#         setattr(db_gem, key,value)
#     session.add(db_gem)
#     session.commit()
#     session.refresh(db_gem)

#     return db_gem

# @gem_router.delete("/{gem_id}", status_code=status.HTTP_202_ACCEPTED)
# def delete_gem(*,session:Session = Depends(get_session), gem_id:int):
#     gem = session.get(Gem,gem_id)
#     if not gem:
#         raise HTTPException(status_code=404, detail="gem not found")
    
#     session.delete(gem)
#     session.commit()
#     return "y se marchó"