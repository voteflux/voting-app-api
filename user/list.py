import json
import os
import pymongo
from mode import *

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[USERSCOLLECTION]]


def list(event, context):
    # create response body object
    response_body = {}

    # create array for reponse users
    response_body['response_users'] = []

    # return path parameters with filter key
    response_body['filter'] = event['multiValueQueryStringParameters']

    # build query with any path parameters
    query = {}
    if event['multiValueQueryStringParameters'] is not None:
        for parameter in event['multiValueQueryStringParameters']:
            query[parameter] = event['multiValueQueryStringParameters'][parameter][0]

    # create list of users
    cursor = collection.find(query)
    for document in cursor:
        response_body['response_users'].append(document)

    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    # return response
    return response
