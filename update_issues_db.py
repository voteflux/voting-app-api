import json
import os
import pymongo
from mode import *
from update_ballotspecs_db import update_ballotspecs


# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[ISSUESCOLLECTION]]

issues = [
    {
        "chamber": "Public",
        "short_title": "Closing of Travel from Coronavirus Countries",
        "start_date": "2019-07-22",
        "end_date": "2020-04-30",
        "question":
        "Should the Australian government look to limit travel from countries affected by Coronavirus?",
        "description":
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "sponsor": "Alexanda the Great",
    },
    {
        "chamber": "Public",
        "short_title": "GST on Sanitary Items",
        "start_date": "2019-09-24",
        "end_date": "2020-07-30",
        "question":
        "Should the Australian government legislate to excluse Sanitary and Health items from the GST?",
        "description":
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "sponsor": "Health Lobby Group",
    },
    {
        "chamber": "Public",
        "short_title": "Legalise Weed",
        "start_date": "2019-05-06",
        "end_date": "2020-08-30",
        "question":
        "Should the Australian government legalise recreational marijuana nationally?",
        "description":
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "sponsor": "Weed Lobby Group",
    },
    {
        "chamber": "Public",
        "short_title": "Independent Anti-corruption Commsion",
        "start_date": "2019-05-01",
        "end_date": "2020-05-30",
        "question": "Should an independent Federal ICAC be created?",
        "description":
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "sponsor": "Freedom Lobby Group",
    },
]


for issue in issues:
    print("-------------------")
    total_issues = len(list(collection.find()))
    print([items for items in list(collection.find())])

    titles = [items["data"]["short_title"] for items in list(collection.find())]
    print(list(titles))
    if issue["short_title"] not in titles:
        if total_issues:
            print([items["num"] for items in list(collection.find())])
            issue_number = collection.find().sort("num", -1)[0]["num"] + 1
            print(issue_number)
        else:
            issue_number = 1
        issue_id = "i" + str(issue_number)
        issue["id"] = issue_id
        collection.insert_one({'_id': issue["id"],
                               "num": issue_number,
                               'data': issue})

        update_ballotspecs(issue["id"], issue["short_title"], issue["question"],
                           issue["description"], issue["start_date"], issue["chamber"], issue["sponsor"])
    else:
        collection.update_one({'data.short_title': issue["short_title"]},
                              {"$set": {'data': issue}}, True)
