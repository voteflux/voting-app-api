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
    url = all_bills[i]["URL"]
    bill = Bill(url)
    # print(bill.data)
    bill.data['Intro House'] = str(bill.data['Intro House'])
    bill.data['Passed House'] = str(bill.data['Passed House'])
    bill.data['Intro Senate'] = str(bill.data['Intro Senate'])
    bill.data['Passed Senate'] = str(bill.data['Passed Senate'])
    bill.data['Assent Date'] = str(bill.data['Assent Date'])
    bill.data['Act No'] = bill.data.pop('Act No.')
    (bill.data['Yes'], bill.data['No']) = get_votes(bill.data["id"])
    # print(bill.data['Assent Date'])
    collection.replace_one({'_id': bill.data["id"]}, {'data': bill.data}, True)
