from mode import *
import pymongo
import os
import json


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


def get_votes(id):
    yes = len(list(votes_collection.find(
        {"data.ballot_id": id, "data.vote": "yes"}, {"_id": 0, "data.vote": 1}))) + 1
    no = len(list(votes_collection.find(
        {"data.ballot_id": id, "data.vote": "no"}, {"_id": 0, "data.vote": 1}))) + 1
    return(yes, no)


def run(event, context):
    # print(all_results)
    for ballot in ballotspecs_collection.find():
        result_doc = {}
        result_doc["_id"] = ballot["_id"]
        result_doc["constituency"] = CONSTITUENCY
        (result_doc["yes"], result_doc["no"]) = get_votes(ballot["_id"])
        print(result_doc["_id"], result_doc["yes"], result_doc["no"])
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
