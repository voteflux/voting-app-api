import json
import logging
import os
from binascii import hexlify

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

log = logging.getLogger(__name__)

def hash_ballotspec(ballotspec_string):
    h = hashlib.sha256()
    h.update(str(ballotspec_string).encode('utf-8'))
    return (h.hexdigest())


def push_to_chain(method, params):
    log.info(f"Pushing to BC API: {json.dumps(params)}")
    r = requests.post("https://api.blockchain.suzuka.flux.party/api", data={"method": method, "params": params})
    log.info(f"push_to_chain Response: {r}\n\n-- Response content {r.content}\n\n-- As text: {r.text}")
    return r


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
        "ballotVersion": 2,
        "optionsVersion": 1,
    }
    ballot_spec_sz = json.dumps(ballotspec_dict)
    bs_h = hash_ballotspec(ballot_spec_sz)

    def render_spec_hash(_s):
        if isinstance(_s, str) or type(_s) is str:
            if _s[:2] != "0x" or len(_s) != 66:
                return "0x" + ("00" * (32 - len(_s)) + hexlify(_s).decode('ascii'))
        return _s

    try:
        # Post to API => posts the blockchain
        push_to_chain("ballot_publish", {
            "specHash": render_spec_hash(id),
            "ballotSpec": ballot_spec_sz,
            "realSpecHash": bs_h
        })
    except Exception as e:
        import traceback
        log.error(f"Error pushing to chain: {e}\n\n{traceback.format_tb(e.__traceback__)}\n\nCONTINUING")

    try:
        ballotspecs_collection.insert_one(
            {'_id': input_dict["id"],
             'data': input_dict,
             BALLOTSPEC_HASH: bs_h})
    except Exception as e:
        print(e)
