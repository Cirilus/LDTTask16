from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

from share.models import Notification, UpdateNotification
from web_server.app.db_methods import get_by_id, get_pending_notifications, update_by_id, delete_by_id, get_db

notification_router = APIRouter()

@notification_router.post(
        "/", 
        response_description="Create a new notification", 
        status_code=status.HTTP_201_CREATED, 
        response_model=Notification)
def create_notification(request: Request, notification: Notification):
    notification = jsonable_encoder(notification)
    new_notification = get_db(request).insert_one(notification)
    created_notification = get_by_id(get_db(request), new_notification.inserted_id)
    return created_notification


@notification_router.get(
        "/{id}",
        response_description="Get notification by id",
        status_code=status.HTTP_200_OK,
        response_model=Notification
)
def get_notification(request: Request, id: str):
    notification = get_by_id(get_db(request), id)
    if notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No notification with id: {id}")
    return notification


@notification_router.put(
        "/{id}",
        response_description="Update user with id",
        status_code=status.HTTP_201_CREATED,
        response_model=Notification
)
def update_notification(request: Request, id: str, notification: UpdateNotification):
    notification = jsonable_encoder(notification)
    if len(notification) >= 1:
        updated = update_by_id(get_db(request), id, notification)
        if updated.modified_count == 1:
            updated_notification = get_by_id(get_db(request), id)
            if updated_notification is not None:
                return updated_notification
    existing_notifications = get_by_id(get_db(request), id)
    if existing_notifications is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No notification with id: {id} found")
    return existing_notifications


@notification_router.delete(
        "/{id}", 
        response_description="Delete a student",
        status_code=status.HTTP_200_OK
)
def delete_notification(request: Request, id: str):
    delete_result =  delete_by_id(get_db(request), id)
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Notification with id: {id} not found")


internal_router = APIRouter()

@internal_router.get(
    "/pending",
    response_description="Get list of notifications needed to be delivered",
    status_code=status.HTTP_200_OK,
    response_model=List[Notification]
)
def get_pending(request: Request):
    pending = get_pending_notifications(get_db(request), datetime.now())
    response = [el for el in pending]
    return response


@internal_router.post(
    "/deactivate",
    response_description="Deactivate List of notifications",
    status_code=status.HTTP_201_ACCEPTED,
    response_model=List[Notification]
)
def deactivate_notifications(request: Request, notifications_ids: List[str]):
    updated_notifications = []
    for id in notifications_ids:
        response = update_by_id(get_db(request), id, {"active": False})
        if response.modified_count == 1:
            updated_notifications.append(get_by_id(get_db(request), id))
    return updated_notifications