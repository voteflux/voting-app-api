import json
import os
import uuid
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[USERSCOLLECTION]]


def create(event, context):
    # get request body
    data = json.loads(event['body'])

    # create user to insert
    user = {
        '_id': str(uuid.uuid1()),
        'data': data,
    }

    # write user to database
    collection.insert_one(user)

    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(user)
    }

    # return response
    return response
