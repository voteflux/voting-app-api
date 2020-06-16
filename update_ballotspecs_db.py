import json
import os
import pymongo
from mode import *
import hashlib
import requests


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

    issue_string = json.dumps(input_dict)

    ballotspec_dict = {
        "ballotTitle": id,
        "longDesc": issue_string,
        "shortDesc": short_title,
        "ballotVersion" : 2,
        "optionsVersion" : 1,
    }
    ballot_spec_sz = json.dumps(ballotspec_dict)
    bs_h = hash_ballotspec(ballot_spec_sz)
    ## Post to the blochain

    to_api = {
        "method": "ballot_publish",
        "params": {
            "specHash": id,
            "ballotSpec": ballot_spec_sz,
            "realSpecHash": bs_h
        }
    }

    print(to_api)
    r = requests.post("https://api.blockchain.suzuka.flux.party/api", data=to_api)
    print(r.text)


    try:
        ballotspecs_collection.insert_one(
            {'_id': input_dict["id"],
             'data': input_dict,
             BALLOTSPEC_HASH: bs_h})

    except Exception as e:
        print(e)
