import json
import os
import pymongo
from mode import *
import hashlib


# Data for each document
ID = "id"
SHORT_TITLE = "short_title"
QUESTION = "question"
DESCRIPTION = "description"
START_DATE = "start_date"
CHAMBER = "chamber"
SPONSOR = "sponsor"
# --- also create
BALLOTSPEC_HASH = "ballotspec_hash"

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
ballotspecs_collection = db[mongosettings[BALLOTSPECSCOLLECTION]]


def hash_ballotspec(ballotspec_string):
    h = hashlib.sha256()
    h.update(str(ballotspec_string).encode('utf-8'))
    return(h.hexdigest())


def update_ballotspecs(id, short_title, question, description, start_date, chamber, sponsor):
    input_dict = {
        ID: id,
        SHORT_TITLE: short_title,
        QUESTION: question,
        DESCRIPTION: description,
        START_DATE: start_date,
        CHAMBER: chamber,
        SPONSOR: sponsor,
    }
    # create ballotspec_hash
    bs_h = hash_ballotspec(json.dumps(input_dict))

    try:
        ballotspecs_collection.insert_one(
            {'_id': input_dict["id"],
             'data': input_dict,
             BALLOTSPEC_HASH: bs_h})
    except Exception as e:
        print(e)
