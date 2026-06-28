from pydantic import BaseModel
from typing import Optional
from app.utils.enums import RequestPriority, RequestStatus


class ServiceRequestCreate(BaseModel):
    title: str
    description: str
    priority: Optional[RequestPriority] = RequestPriority.MEDIUM


class ServiceRequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[RequestPriority] = None


class ServiceRequestAssign(BaseModel):
    assigned_to: str


class ServiceRequestStatusUpdate(BaseModel):
    status: RequestStatus


class ServiceRequestResponse(BaseModel):
    id: str
    title: str
    description: str
    priority: RequestPriority
    status: RequestStatus
    created_by: Optional[str]
    assigned_to: Optional[str]
    created_at: str


class DashboardSummaryResponse(BaseModel):
    total_requests: int
    open: int
    assigned: int
    in_progress: int
    resolved: int
    closed: int
