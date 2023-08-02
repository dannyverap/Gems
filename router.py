from fastapi import Depends,APIRouter, status, HTTPException, Query

gem_router = APIRouter()


@gem_router.get("/")
def hello():
    return "Hello World!"