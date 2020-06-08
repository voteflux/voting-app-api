import json
import os
import uuid
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[RESULTSCOLLECTION]]


def create(event, context):
    # get request body
    data = json.loads(event['body'])

    # create result to insert
    result = {
        '_id': data["id"],
        'data': data,
    }

    # write result to database
    collection.insert_one(result)

    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    # return response
    return response
