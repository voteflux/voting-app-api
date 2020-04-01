import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[USERSCOLLECTION]]


def get(event, context):
    # get bill_id to delete from path parameter
    bill_id = event['pathParameters']['id']

    # delete bill from the database
    bill = collection.find_one({"_id": bill_id})

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(bill)
    }

    # return response
    return response
