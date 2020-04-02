import json
import os
import uuid
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[BILLSCOLLECTION]]


def create(event, context):
    # get request body
    data = json.loads(event['body'])

    # create bill to insert
    bill = {
        '_id': data["id"],
        'data': data,
    }

    # write bill to database
    collection.insert_one(bill)

    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(bill)
    }

    # return response
    return response
