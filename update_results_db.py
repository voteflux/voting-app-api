from mode import *
import pymongo
import os
import json
from read_blockchain import get_votes_from_blochchain


# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
results_collection = db[mongosettings[RESULTSCOLLECTION]]
ballotspecs_collection = db[mongosettings[BALLOTSPECSCOLLECTION]]
votes_collection = db[mongosettings[VOTESCOLLECTION]]
bills_collection = db[mongosettings[BILLSCOLLECTION]]
issues_collection = db[mongosettings[ISSUESCOLLECTION]]
CONSTITUENCY = "Australia"

# dummy function, waiting for votes to be counted on the blockchain.


def get_votes(spec_hash):
    (yes, no) = get_votes_from_blochchain(spec_hash)
    if yes == 0:
        yes = 1
    if no == 0:
        no = 1
    return(yes, no)


def run(event, context):
    # print(all_results)
    for ballot in ballotspecs_collection.find():
        result_doc = {}
        result_doc["_id"] = ballot["_id"]
        result_doc["constituency"] = CONSTITUENCY
        (result_doc["yes"], result_doc["no"]) = get_votes("0x"+ballot["ballotspec_hash"])
        # print(result_doc["_id"], result_doc["yes"], result_doc["no"])
        results_collection.replace_one({'_id': result_doc["_id"]}, {'data': result_doc}, True)
        if result_doc["constituency"] == CONSTITUENCY:
            if result_doc["_id"][0] == "i":
                issues_collection.update_one({'_id': result_doc["_id"]},
                                             {"$set": {"data.yes": result_doc["yes"]}})
                issues_collection.update_one({'_id': result_doc["_id"]},
                                             {"$set": {"data.no": result_doc["no"]}})
            elif result_doc["_id"][0] == "s" or result_doc["_id"][0] == "r":
                bills_collection.update_one({'_id': result_doc["_id"]},
                                            {"$set": {"data.yes": result_doc["yes"]}})
                bills_collection.update_one({'_id': result_doc["_id"]},
                                            {"$set": {"data.no": result_doc["no"]}})
