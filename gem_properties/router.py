from fastapi import APIRouter

gem_properties_router = APIRouter()


@gem_properties_router.get("/")
def hello():
    return "Hello World! 3"