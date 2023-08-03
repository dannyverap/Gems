from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session
from gem_properties.schema import GemPropertiesCreate, GemPropertiesRead, GemPropertiesUpdate
from typing import List
from gem_properties.service import *
from dependencies import get_db

gem_properties_router = APIRouter()

@gem_properties_router.post("/", response_model=GemPropertiesRead,status_code=status.HTTP_201_CREATED)
def create_gem_properties(*,db:Session = Depends(get_db), gem_properties:GemPropertiesCreate):
    new_gem_properties = service_create(db, gem_properties)
    return new_gem_properties 

@gem_properties_router.get("/all", response_model=List[GemPropertiesRead], status_code=status.HTTP_200_OK)
def get_gem_properties(
    *,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    gem_properties = service_get_gem_properties(db, offset, limit)
    return gem_properties

@gem_properties_router.get("/{gem_properties_id}", response_model=GemPropertiesRead, status_code=status.HTTP_200_OK)
def get_gem_properties_by_id(*,db: Session = Depends(get_db) ,gem_properties_id:int):
    gem_properties = service_get_by_id(db, id=gem_properties_id)
    if not gem_properties:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="gem_properties not found")
    return gem_properties

@gem_properties_router.patch("/{gem_properties_id}", response_model=GemPropertiesRead,status_code=status.HTTP_200_OK)
def update_gem_properties (*,db:Session=Depends(get_db), gem_properties_id:int, gem_properties:GemPropertiesUpdate):
    db_gem_properties = service_get_by_id(db,id=gem_properties_id)
    if not db_gem_properties :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="gem_properties not found")
    
    updated_gem_properties = service_update_gem_properties (db,gem_properties,db_gem_properties )
    return updated_gem_properties 

@gem_properties_router.delete("/{gem_properties_id}", status_code=status.HTTP_200_OK)
def delete_gem_properties (*,db:Session=Depends(get_db), gem_properties_id:int):
    db_gem_properties = service_get_by_id(db,id=gem_properties_id)
    if not db_gem_properties :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="gem_properties not found")
    return service_delete(db,db_gem_properties )
