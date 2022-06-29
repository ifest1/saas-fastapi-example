from fastapi import APIRouter, HTTPException, Request, status
from app.core.utils import create_tenant_migration
from app.models.tenants import Tenant


router = APIRouter()


@router.post("/", response_model=Tenant, status_code=201)
async def create_tenant(tenant: Tenant, request: Request):
    await tenant.save()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create tenant.",
        )
    create_tenant_migration(tenant.name)
    return tenant
