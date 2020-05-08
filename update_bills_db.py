
import random
from mode import *
import pymongo
import os
from ausbills.federal_parliment import all_bills, Bill
import json
from update_ballotspecs_db import update_ballotspecs


# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
bills_collection = db[mongosettings[BILLSCOLLECTION]]


# dummy function, waiting for votes to be counted on the blockchain.
def get_votes(id):
    return(500 + int(random.random()*1000), 500 + int(random.random()*1000))


naughty_words = ['corona', 'covid']
# print(all_bills)
bad_bills = []


def run(event, context):
    for i in range(len(all_bills)):
        post = True
        print(all_bills[i]["id"])
        url = all_bills[i]["url"]
        bill = Bill(url)
        # Standed keys
        bill.data["question"] = "Should this bill be passed into law?"
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
    for bill in bad_bills:
        print(bad_bills)


badbills = [('r6524', 'Appropriation (Coronavirus Economic Response Package) (No. 1) 2019-2020'), ('r6530', 'Appropriation (Coronavirus Economic Response Package) (No. 2) 2019-2020'), ('r6532', 'Appropriation (No. 5) 2019-2020'), ('r6534', 'Appropriation (No. 6) 2019-2020'), ('r6523', 'Assistance for Severely Affected Regions (Special Appropriation) (Coronavirus Economic Response Package) 2020'), ('r6519', 'Australian Business Growth Fund (Coronavirus Economic Response Package) 2020'), ('r6522',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'Boosting Cash Flow for Employers (Coronavirus Economic Response Package) 2020'), ('r6521', 'Coronavirus Economic Response Package Omnibus 2020'), ('r6535', 'Coronavirus Economic Response Package Omnibus (Measures No. 2) 2020'), ('r6533', 'Coronavirus Economic Response Package (Payments and Benefits) 2020'), ('r6529', 'Guarantee of Lending to Small and Medium Enterprises (Coronavirus Economic Response Package) 2020'), ('r6528', 'Structured Finance Support (Coronavirus Economic Response Package) 2020')]

for bill in badbills:
    print(bill)
