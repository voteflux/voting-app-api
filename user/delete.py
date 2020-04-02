import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[USERSCOLLECTION]]


def delete(event, context):
    # get user_id to delete from path parameter
    user_id = event['pathParameters']['id']

    # delete user from the database
    del_resp = collection.delete_one({"_id": user_id})

    # if no user return 404
    if del_resp.deleted_count == 0:

        response = {
            "statusCode": 404,
        }

        return response

    # create a response
    response = {
        "statusCode": 204,
    }

    return response
