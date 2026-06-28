from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.service_requests import router as service_requests_router
from app.routers.dashboard import router as dashboard_router

app = FastAPI(
    title="Service Request Management System",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(service_requests_router)
app.include_router(dashboard_router)


@app.get("/")
def health_check():
    return {
        "message": "API Running Successfully"
    }