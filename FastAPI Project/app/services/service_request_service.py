import uuid
from fastapi import HTTPException
from app.core.supabase_client import supabase
from app.utils.enums import UserRole
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate


def create_request(data: ServiceRequestCreate, user_id: str):
    request_id = str(uuid.uuid4())
    new_request = {
        "id": request_id,
        "title": data.title,
        "description": data.description,
        "priority": data.priority.value if hasattr(data.priority, "value") else data.priority,
        "status": "OPEN",
        "created_by": user_id,
        "assigned_to": None
    }
    
    response = supabase.table("service_requests").insert(new_request).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create service request")
    return response.data[0]


def get_requests(current_user: dict):
    role = current_user.get("role")
    user_id = current_user.get("sub")
    
    if role == UserRole.ADMIN:
        response = supabase.table("service_requests").select("*").execute()
    elif role == UserRole.TECHNICIAN:
        response = supabase.table("service_requests").select("*").eq("assigned_to", user_id).execute()
    else:  # USER
        response = supabase.table("service_requests").select("*").eq("created_by", user_id).execute()
        
    return response.data or []


def get_request_by_id(request_id: str, current_user: dict):
    response = supabase.table("service_requests").select("*").eq("id", request_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Service request not found")
        
    req = response.data[0]
    role = current_user.get("role")
    user_id = current_user.get("sub")
    
    if role == UserRole.ADMIN:
        return req
    elif role == UserRole.TECHNICIAN:
        if req.get("assigned_to") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this request")
        return req
    else:  # USER
        if req.get("created_by") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this request")
        return req


def update_request(request_id: str, data: ServiceRequestUpdate, current_user: dict):
    # Fetch request first to check access permissions
    req = get_request_by_id(request_id, current_user)
    role = current_user.get("role")
    
    if role == UserRole.TECHNICIAN:
        raise HTTPException(status_code=403, detail="Technicians cannot modify request details")
        
    update_data = {}
    if data.title is not None:
        update_data["title"] = data.title
    if data.description is not None:
        update_data["description"] = data.description
    if data.priority is not None:
        update_data["priority"] = data.priority.value if hasattr(data.priority, "value") else data.priority
        
    if not update_data:
        return req
        
    response = supabase.table("service_requests").update(update_data).eq("id", request_id).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to update request")
    return response.data[0]


def delete_request(request_id: str, current_user: dict):
    # Fetch request first to check access permissions
    get_request_by_id(request_id, current_user)
    role = current_user.get("role")
    
    if role == UserRole.TECHNICIAN:
        raise HTTPException(status_code=403, detail="Technicians cannot delete requests")
        
    response = supabase.table("service_requests").delete().eq("id", request_id).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to delete request")
    return True


def assign_request(request_id: str, technician_id: str):
    # Check if target technician exists in database
    tech_check = supabase.table("users").select("*").eq("id", technician_id).execute()
    if not tech_check.data:
        raise HTTPException(status_code=400, detail="Technician user not found")
        
    user_data = tech_check.data[0]
    if user_data.get("role") != UserRole.TECHNICIAN:
        raise HTTPException(status_code=400, detail="User is not a technician")
        
    # Check if request exists
    req_check = supabase.table("service_requests").select("*").eq("id", request_id).execute()
    if not req_check.data:
        raise HTTPException(status_code=404, detail="Service request not found")
        
    update_data = {
        "assigned_to": technician_id,
        "status": "ASSIGNED"
    }
    
    response = supabase.table("service_requests").update(update_data).eq("id", request_id).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to assign request")
    return response.data[0]


def update_request_status(request_id: str, status: str, current_user: dict):
    # Check if request exists
    req_check = supabase.table("service_requests").select("*").eq("id", request_id).execute()
    if not req_check.data:
        raise HTTPException(status_code=404, detail="Service request not found")
        
    req = req_check.data[0]
    role = current_user.get("role")
    user_id = current_user.get("sub")
    
    if role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Users cannot update request status")
    elif role == UserRole.TECHNICIAN:
        if req.get("assigned_to") != user_id:
            raise HTTPException(status_code=403, detail="Technicians can only update status for assigned requests")
            
    update_data = {
        "status": status.value if hasattr(status, "value") else status
    }
    
    response = supabase.table("service_requests").update(update_data).eq("id", request_id).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to update request status")
    return response.data[0]


def get_dashboard_summary():
    response = supabase.table("service_requests").select("status").execute()
    data = response.data or []
    total = len(data)
    
    summary = {
        "total_requests": total,
        "open": sum(1 for r in data if r.get("status") == "OPEN"),
        "assigned": sum(1 for r in data if r.get("status") == "ASSIGNED"),
        "in_progress": sum(1 for r in data if r.get("status") == "IN_PROGRESS"),
        "resolved": sum(1 for r in data if r.get("status") == "RESOLVED"),
        "closed": sum(1 for r in data if r.get("status") == "CLOSED")
    }
    return summary


def get_my_tasks(current_user: dict):
    user_id = current_user.get("sub")
    role = current_user.get("role")
    
    if role == UserRole.ADMIN:
        response = supabase.table("service_requests").select("*").execute()
        data = response.data or []
        return [r for r in data if r.get("created_by") == user_id or r.get("assigned_to") == user_id]
    elif role == UserRole.TECHNICIAN:
        response = supabase.table("service_requests").select("*").eq("assigned_to", user_id).execute()
        return response.data or []
    else:  # USER
        response = supabase.table("service_requests").select("*").eq("created_by", user_id).execute()
        return response.data or []
