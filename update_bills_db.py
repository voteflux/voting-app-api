import json
from ausbills.federal_parliment import all_bills, Bill
import os
import pymongo
from mode import *
import random

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[BILLSCOLLECTION]]


# dummy function, waiting for votes to be counted on the blockchain.
def get_votes(id):
    return(500 + int(random.random()*1000), 500 + int(random.random()*1000))


# print(all_bills)
for i in range(len(all_bills)):
    print(all_bills[i]["id"])
    url = all_bills[i]["url"]
    bill = Bill(url)
    (bill.data['yes'], bill.data['no']) = get_votes(bill.data["id"])
    bill.data['ballotspec_hash'] = "COWIBY3978QCNYOXIURY3B8O7T5CNOQ8XW37C5N89347TY"
    # print(bill.data['Assent Date'])
    collection.replace_one({'_id': bill.data["id"]}, {'data': bill.data}, True)
