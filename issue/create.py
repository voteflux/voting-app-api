import json
import os
import uuid
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[ISSUESCOLLECTION]]


def create(event, context):
    # get request body
    data = json.loads(event['body'])

    # create issue to insert
    issue = {
        '_id': data["id"],
        'data': data,
    }

    # write issue to database
    collection.insert_one(issue)

    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(issue)
    }

    # return response
    return response
