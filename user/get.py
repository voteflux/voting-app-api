import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[USERSCOLLECTION]]


def get(event, context):
    # get user_id to delete from path parameter
    user_id = event['pathParameters']['id']

    # delete user from the database
    user = collection.find_one({"_id": user_id})

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(user)
    }

    # return response
    return response
