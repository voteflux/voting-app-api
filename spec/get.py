import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[BALLOTSPECSCOLLECTION]]


def get(event, context):
    ballotspec_id = event['pathParameters']['id']
    ballot = collection.find_one({"_id": ballotspec_id})

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(ballot)
    }

    # return response
    return response
