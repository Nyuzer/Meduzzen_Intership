from fastapi import APIRouter
from routers import users_routers, auth_router, companies_routers, actions_routers, quizzes_routers, analitics_routers


routes = APIRouter()

routes.include_router(users_routers.router, prefix='/users')
routes.include_router(auth_router.router, prefix='/auth')
routes.include_router(companies_routers.router, prefix='/company')
routes.include_router(actions_routers.router, prefix='/invite')
routes.include_router(quizzes_routers.router, prefix='/quizz')
routes.include_router(analitics_routers.router, prefix='/analytic')
