from fastapi import FastAPI, Request
from datetime import datetime

from app.api import connect_to_db
from app.api import Notification
from .routers import notification_router, internal_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = connect_to_db()
    app.database = app.mongodb_client["notifications_db"]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(notification_router, tags=["notifications"], prefix="/notifications")
app.include_router(internal_router, tags=["notifications", "server"], prefix="/internal")