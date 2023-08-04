from fastapi import APIRouter, status, Depends, HTTPException, Query, responses
from sqlmodel import Session
from typing import List
from dependencies import get_db
from user.schema import UserLogin
from user.service import *
from auth.auth import AuthHandler


auth_router = APIRouter()
auth_handler = AuthHandler()


@auth_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(*, db: Session = Depends(get_db), user: UserLogin):
    user_found = service_get_by_username(db, username=user.username)
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    verified_password = auth_handler.verify_password(user.password, user_found.password)
    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    token = auth_handler.encode_token(user_found.username)
    return {"token": token}
