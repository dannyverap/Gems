from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from create_db import create_db_and_tables
from gem.router import gem_router
from gem_properties.router import gem_properties_router
from user.router import user_router
from auth.router import auth_router



app = FastAPI(
    title="Proyecto de Danny",
    description="Lista de regalos",
    version="0.0.1",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


app.include_router(gem_router, prefix="/gem", tags=["Gem"])
app.include_router(gem_properties_router, prefix="/properties", tags=["Gem Properties"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router,prefix="/auth", tags=["Auth"])