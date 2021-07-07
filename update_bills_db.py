
import random
from mode import *
import pymongo
import os
from ausbills.federal_parliment import all_bills, Bill
import json
from update_ballotspecs_db import update_ballotspecs
from tag_topics import tag_bill


def run(event, context):
    # Connection String
    client = pymongo.MongoClient(mongosettings[URL])
    db = client[mongosettings[MONGODB]]
    bills_collection = db[mongosettings[BILLSCOLLECTION]]
    # ! this is a quick fix for the google ban on covid apps
    naughty_words = ['corona', 'covid']
    bad_bills = []
    for i in range(len(all_bills)):
        post = True
        # print(all_bills[i]["id"])
        url = all_bills[i]["url"]
        bill = Bill(url)
        # Standed keys
        bill.data["question"] = "Should this bill be passed into law?"
        bill.data["topics"] = tag_bill(bill.data)
        bill.data["description"] = bill.data.pop("summary")
        if bill.data["chamber"] == "House":
            bill.data["start_date"] = bill.data["intro_house"]
        else:
            bill.data["start_date"] = bill.data["intro_senate"]

        for word in naughty_words:
            if word in bill.data["description"].lower() or word in bill.data["short_title"].lower():
                post = False
                print(bill.data["id"],  bill.data["short_title"])

        if post:
            update_ballotspecs(bill.data["id"], bill.data["short_title"], bill.data["question"],
                               bill.data["description"], bill.data["start_date"], bill.data["chamber"], bill.data["sponsor"])

            bills_collection.replace_one({'_id': bill.data["id"]}, {'data': bill.data}, True)
        else:
            bad_bills.append((bill.data["id"],  bill.data["short_title"]))

