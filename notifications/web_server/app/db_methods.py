from pymongo import MongoClient, collection
from pymongo.errors import ConnectionFailure,WriteConcernError
from datetime import datetime
from fastapi import HTTPException, status
from ...share.models import Notification

def connect_to_db():
    try:
        client = MongoClient(host='notifications_db',
                         port=27017, 
                         username='admin', 
                         password='admin',
                         authSource="admin")
        return client
    except ConnectionFailure:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't connect to db")
    
def get_db(request, db_name="notifications"):
    return request.app.database[db_name]


def get_pending_notifications(db_connection, target_date: datetime):
    items = db_connection.find(
        {
            "ts": {"$lte": str(target_date)},
            "active": True
         }
    )
    return items

def get_by_id(db_connection, id:str):
    item = db_connection.find_one(
        {"_id":id}
    )
    return item

def update_by_id(db_connection, id: str, val):
    response = db_connection.update_one(
        {"_id": id},
        {"$set": val}
    )
    return response

def delete_by_id(db_connection, id: str):
    response = db_connection.delete_one(
        {"_id": id}
    )
    return response