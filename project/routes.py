from fastapi import APIRouter
from routers import users_routers, auth_router


routes = APIRouter()

routes.include_router(users_routers.router, prefix='/users')
routes.include_router(auth_router.router, prefix='/auth')
