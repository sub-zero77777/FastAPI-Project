import uuid

from app.core.supabase_client import supabase
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token


def register_user(user_data):

    existing_user = (
        supabase
        .table("users")
        .select("*")
        .eq("email", user_data.email)
        .execute()
    )

    if existing_user.data:
        raise Exception("Email already exists")

    user = {
        "id": str(uuid.uuid4()),
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hash_password(
            user_data.password
        ),
        "role": "USER"
    }

    supabase.table("users").insert(user).execute()

    return user


def login_user(email: str, password: str):

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not response.data:
        return None

    user = response.data[0]

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    token = create_access_token(
        {
            "sub": user["id"],
            "email": user["email"],
            "role": user["role"]
        }
    )

    return token