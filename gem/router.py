from fastapi import APIRouter, status, Depends, HTTPException, Query,responses
from sqlmodel import Session
from gem.schema import GemCreate, GemRead, GemUpdate, GemWithProperties
from typing import List
from gem.service import *
from dependencies import get_db
from user.router import auth_handler

gem_router = APIRouter()


@gem_router.post("/", response_model=GemWithProperties,status_code=status.HTTP_201_CREATED)
def create_gem(*,db:Session = Depends(get_db), gem:GemCreate, user= Depends(auth_handler.get_current_user)):
    
    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Not a seller")

    if gem.seller_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allow to create other's gems")
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

@gem_router.get("/seller/me", response_model=List[GemWithProperties],status_code=status.HTTP_200_OK)
def get_all_my_gems(
    *,db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    user= Depends(auth_handler.get_current_user),
    ):
    
    if not user.is_seller:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Not a seller")
    
    gems = service_get_gems_by_user(db,offset,limit,user_id=user.id)
    return gems


@gem_router.get("/{gem_id}", response_model=GemWithProperties, status_code=status.HTTP_200_OK)
def get_gem_by_id(*,db: Session = Depends(get_db) ,gem_id:int, user= Depends(auth_handler.get_current_user)):
    gem = service_get_by_id(db, id=gem_id)
    if not gem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gem not found")
    if gem.seller_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allow to see other's gems")
    return gem

@gem_router.patch("/{gem_id}", response_model=GemWithProperties,status_code=status.HTTP_200_OK)
def update_gem(*,db:Session=Depends(get_db), gem_id:int, gem:GemUpdate, user= Depends(auth_handler.get_current_user)):
    if gem.seller_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allow to modify other's gems")
    
    db_gem = service_get_by_id(db,id=gem_id)
    if not db_gem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gem not found")
    
    updated_gem = service_update_gem(db,gem,db_gem)
    return updated_gem

@gem_router.delete("/{gem_id}", status_code=status.HTTP_200_OK)
def delete_gem(*,db:Session=Depends(get_db), gem_id:int, user= Depends(auth_handler.get_current_user)):
    db_gem = service_get_by_id(db,id=gem_id)
    if not db_gem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gem not found")
    if db_gem.seller_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not allow to delete other's gems")
    
    return service_delete(db,db_gem)
