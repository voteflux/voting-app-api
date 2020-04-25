import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[ISSUESCOLLECTION]]


def list(event, context):
    # create response body object
    response_body = []

    # create list of issues
    cursor = collection.find()
    for document in cursor:
        response_body.append(document)

    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    # return response
    return response
