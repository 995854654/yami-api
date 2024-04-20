from fastapi import APIRouter

home_router = APIRouter(
    tags=["home"],
    include_in_schema=True
)


@home_router.get("/")
def root():
    return {"msg": "Welcome to the yami-api!!!"}
