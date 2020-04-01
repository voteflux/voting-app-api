import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[MONGOCOLLECTION]]


def delete(event, context):
    # get bill_id to delete from path parameter
    bill_id = event['pathParameters']['id']

    # delete bill from the database
    del_resp = collection.delete_one({"_id": bill_id})

    # if no bill return 404
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
