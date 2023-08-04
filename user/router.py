from fastapi import APIRouter, status, Depends, HTTPException, Query,responses
from sqlmodel import Session
from user.schema import UserCreate, UserRead, UserUpdate
from typing import List
from user.service import *
from dependencies import get_db

user_router = APIRouter()

@user_router.post("/", response_model=UserRead,status_code=status.HTTP_201_CREATED)
def create_user(*,db:Session = Depends(get_db), user:UserCreate):
    new_user = service_create(db, user)
    return new_user

@user_router.get("/all", response_model=List[UserRead], status_code=status.HTTP_200_OK)
def get_users(
    *,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    users = service_get_users(db, offset, limit)
    return users

@user_router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user_by_id(*,db: Session = Depends(get_db) ,user_id:int):
    user = service_get_by_id(db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@user_router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(*,db:Session=Depends(get_db), user_id:int, user:UserUpdate):
    db_user = service_get_by_id(db,id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    updated_user = service_update_user(db,user,db_user)
    return updated_user

@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(*,db:Session=Depends(get_db), user_id:int):
    db_user = service_get_by_id(db,id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return service_delete(db,db_user)
