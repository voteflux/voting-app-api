import json
import os
import uuid
import pymongo
from mode import *
import hashlib


# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[VOTESCOLLECTION]]


def create(event, context):
    # get request body
    data = json.loads(event['body'])

    try:
        # create vote to insert
        vote_id = make_vote_id(data["pub_key"], data["ballot_id"],
                               data["ballotspec_hash"], data["constituency"])
        assert data["vote"] == "yes" or data["vote"] == "no"
        vote = {
            "_id": vote_id,
            "data": data,
        }

        # write bill to database
        collection.replace_one({'_id': vote_id}, {'data': data}, True)

        # create response
        response = {
            "statusCode": 200,
            "body": json.dumps(vote)
        }
    except Exception as e:
        response = {
            "statusCode": 400,
            "body": str(e),
        }

    # return response
    return response


def make_vote_id(pub_key, id, ballotspec_hash, constituency):
    h = hashlib.sha256()
    h.update(str(pub_key).encode('utf-8') +
             str(id).encode('utf-8') +
             str(ballotspec_hash).encode('utf-8') +
             str(constituency).encode('utf-8'))
    return(h.hexdigest())
