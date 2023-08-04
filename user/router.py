from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session
from user.schema import UserCreate, UserRead, UserUpdate
from typing import List
from user.service import *
from dependencies import get_db
from auth.auth import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(get_db), user: UserCreate):
    username_in_db = service_get_by_username(db, username=user.username)
    email_in_db = service_get_by_email(db, email=user.email)
    if username_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already taken"
        )

    if email_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken"
        )

    user.password = auth_handler.get_password_hash(user.password)
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

@user_router.get('/me', status_code=status.HTTP_200_OK, response_model=UserRead)
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user

@user_router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user_by_id(*, db: Session = Depends(get_db), user_id: int):
    user = service_get_by_id(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@user_router.patch("/", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_current_user(*, db: Session = Depends(get_db), user: UserUpdate, current_user: User = Depends(auth_handler.get_current_user)):
    db_user = service_get_by_id(db, id=current_user.id)
    # if not db_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #     )

    updated_user = service_update_user(db, user, db_user)
    return updated_user


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(*, db: Session = Depends(get_db), user_id: int, current_user: User = Depends(auth_handler.get_current_user)):
    db_user = service_get_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")
    return service_delete(db, db_user)
