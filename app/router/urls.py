from fastapi import APIRouter
from app.endpoints import student

api_router = APIRouter()

api_router.include_router(student.router, prefix="/students", tags=["students"])
