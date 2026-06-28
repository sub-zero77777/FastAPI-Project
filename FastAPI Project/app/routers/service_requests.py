from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.core.dependencies_rbac import require_role
from app.utils.enums import UserRole
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestUpdate,
    ServiceRequestAssign,
    ServiceRequestStatusUpdate,
    ServiceRequestResponse,
)
from app.services.service_request_service import (
    create_request,
    get_requests,
    get_request_by_id,
    update_request,
    delete_request,
    assign_request,
    update_request_status,
)

router = APIRouter(
    prefix="/requests",
    tags=["Service Requests"]
)


@router.post("", response_model=ServiceRequestResponse)
def create(
    payload: ServiceRequestCreate,
    current_user=Depends(require_role([UserRole.ADMIN, UserRole.USER]))
):
    return create_request(payload, current_user["sub"])


@router.get("", response_model=list[ServiceRequestResponse])
def get_all(
    current_user=Depends(get_current_user)
):
    return get_requests(current_user)


@router.get("/{id}", response_model=ServiceRequestResponse)
def get_by_id(
    id: str,
    current_user=Depends(get_current_user)
):
    return get_request_by_id(id, current_user)


@router.put("/{id}", response_model=ServiceRequestResponse)
def update(
    id: str,
    payload: ServiceRequestUpdate,
    current_user=Depends(require_role([UserRole.ADMIN, UserRole.USER]))
):
    return update_request(id, payload, current_user)


@router.delete("/{id}")
def delete(
    id: str,
    current_user=Depends(require_role([UserRole.ADMIN, UserRole.USER]))
):
    delete_request(id, current_user)
    return {"message": "Service request deleted successfully"}


@router.put("/{id}/assign", response_model=ServiceRequestResponse)
def assign(
    id: str,
    payload: ServiceRequestAssign,
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return assign_request(id, payload.assigned_to)


@router.put("/{id}/status", response_model=ServiceRequestResponse)
def update_status(
    id: str,
    payload: ServiceRequestStatusUpdate,
    current_user=Depends(require_role([UserRole.ADMIN, UserRole.TECHNICIAN]))
):
    return update_request_status(id, payload.status, current_user)
