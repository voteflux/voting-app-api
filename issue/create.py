import json
import os
import uuid
import pymongo
from mode import *
from update_ballotspecs_db import update_ballotspecs

# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
collection = db[mongosettings[ISSUESCOLLECTION]]


issues_document = {"_id": "i4",
                   "num": 4,
                   "data": {"chamber": "Public",
                            "short_title": "Independent Anti-corruption Commsion",
                            "start_date": "2019-05-01",
                            "end_date": "2020-05-30",
                            "question": "Should an independent Federal ICAC be created?",
                            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", "sponsor": "Freedom Lobby Group"}}


def create(event, context):
    # get request body
    try:
        payload = json.loads(event['body'])

        TOKEN = payload["token"]

        if ISSUE_TOKEN == TOKEN:

            issue = payload["data"]

            total_issues = len(list(collection.find()))

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
                response = {
                    "statusCode": 200,
                    "body": json.dumps(issue)
                }
            else:
                # collection.update_one({'data.short_title': issue["short_title"]},
                #                       {"$set": {'data': issue}}, True)

                response = {
                    "statusCode": 409,
                    "body": json.dumps("short_title already exists")
                }
        elif TOKEN == 'TEST':
            
            issue = payload["data"]

            response = {
                "statusCode": 200,
                "body": json.dumps(issue)
            }

        else:
            response = {
                "statusCode": 401,
                "body": json.dumps("Invalid token")
            }

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": str(e)
        }
    # return response
    return response
