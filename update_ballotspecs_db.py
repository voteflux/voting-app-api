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
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = pymongo.MongoClient(mongosettings[URL])
    return _client


log = logging.getLogger(__name__)


def hash_ballotspec(ballotspec_string):
    h = hashlib.sha256()
    h.update(str(ballotspec_string).encode('utf-8'))
    return (h.hexdigest())


def push_to_chain(method, params):
    log.info(f"Pushing to BC API: {json.dumps(params)}")
    print(method)
    print(params)
    r = requests.post("https://api.blockchain.suzuka.flux.party/members/api", data=json.dumps({"method": method, "params": params}))
    print(r.text)
    log.info(f"push_to_chain Response: {r}\n\n-- Response content {r.content}\n\n-- As text: {r.text}")
    return json.loads(r.text)["billCreationTxid"]


def render_spec_hash(_s):
    if isinstance(_s, str) or type(_s) is str:
        if _s[:2] != "0x" or len(_s) != 66:
            return "0x" + ("00" * (32 - len(_s)) + hexlify(_s.encode()).decode())
    return _s

def update_ballotspecs(id, short_title, question, description, start_date, chamber, sponsor):
    db = _get_client()[mongosettings[MONGODB]]
    ballotspecs_collection = db[mongosettings[BALLOTSPECSCOLLECTION]]
    bills_collection = db[mongosettings[BILLSCOLLECTION]]

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

    try:
        # Post to API => posts the blockchain
        TxID = push_to_chain("ballot_publish", {
            "specHash": bs_h, #render_spec_hash(id),
            "ballotSpec": ballot_spec_sz,
            "realSpecHash": bs_h
        })
        print("Bill")
        print(bs_h)
        print(TxID)
    except Exception as e:
        import traceback
        log.error(f"Error pushing to chain: {e}\n\n{traceback.format_tb(e.__traceback__)}\n\nCONTINUING")

    try:
        ballotspecs_collection.insert_one(
            {'_id': input_dict["id"],
             'data': input_dict,
             BALLOTSPEC_HASH: bs_h,
            #  "tx_id" : TxID,
             "specHash": bs_h,
             "ballotSpec": ballot_spec_sz,
             "realSpecHash": bs_h})
    except Exception as e:
        print(e)