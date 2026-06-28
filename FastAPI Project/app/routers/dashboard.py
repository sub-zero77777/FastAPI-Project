from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.core.dependencies_rbac import require_role
from app.utils.enums import UserRole
from app.schemas.service_request import (
    DashboardSummaryResponse,
    ServiceRequestResponse,
)
from app.services.service_request_service import (
    get_dashboard_summary,
    get_my_tasks,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary", response_model=DashboardSummaryResponse)
def summary(
    current_user=Depends(require_role([UserRole.ADMIN]))
):
    return get_dashboard_summary()


@router.get("/my-tasks", response_model=list[ServiceRequestResponse])
def my_tasks(
    current_user=Depends(get_current_user)
):
    return get_my_tasks(current_user)
