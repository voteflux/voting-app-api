import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[ISSUESCOLLECTION]]


def get(event, context):
    # get issue_id to delete from path parameter
    issue_id = event['pathParameters']['id']

    # delete issue from the database
    issue = collection.find_one({"_id": issue_id})

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(issue)
    }

    # return response
    return response
