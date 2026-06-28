from fastapi import Depends, HTTPException
from app.core.dependencies import get_current_user
from app.utils.enums import UserRole


def require_role(allowed_roles: list[str]):
    def dependency(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if not user_role or user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted for this role"
            )
        return current_user
    return dependency
