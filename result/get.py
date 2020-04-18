import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[RESULTSCOLLECTION]]


def get(event, context):
    # get result_id to delete from path parameter
    result_id = event['pathParameters']['id']

    # delete result from the database
    result = collection.find_one({"_id": result_id})

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    # return response
    return response
