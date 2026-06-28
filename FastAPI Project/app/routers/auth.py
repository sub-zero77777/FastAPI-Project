from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.auth import UserRegister
from app.schemas.auth import UserLogin

from app.services.auth_service import register_user
from app.services.auth_service import login_user
from fastapi import Depends

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(payload: UserRegister):

    try:

        user = register_user(payload)

        return {
            "message": "User registered successfully",
            "user_id": user["id"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(payload: UserLogin):

    token = login_user(
        payload.email,
        payload.password
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user