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
