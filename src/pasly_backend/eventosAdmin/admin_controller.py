from fastapi import APIRouter
from .admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])
service = AdminService()


@router.post("/")
async def create_evento():
    return service.create_evento()