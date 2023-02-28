from fastapi import APIRouter
from routers import users_routers


routes = APIRouter()

routes.include_router(users_routers.router, prefix='/users')
