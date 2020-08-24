import os

USER = 'user'
PWD = 'pwd'
MONGODB = 'mongodb'
BILLSCOLLECTION = 'billscollection'
ISSUESCOLLECTION = 'issuescollection'
RESULTSCOLLECTION = 'resultscollection'
USERSCOLLECTION = 'userscollection'
VOTESCOLLECTION = 'votescollection'
BALLOTSPECSCOLLECTION = "ballotspecscollection"
URL = 'url'

user = os.environ['MONGO_DB_USER']
pwd = os.environ['MONGO_DB_PASS']
url = os.environ['MONGO_DB_URL']
ISSUE_TOKEN = os.environ['ISSUE_CREATE_TOKEN']

print(user, url, pwd)
if user is not None and pwd is not None:
    cluster = True
else:
    cluster = False

# cluster = False

ms = {
    # MONGODB: os.environ['MONGO_DB_NAME'],
    # MONGOCOLLECTION: os.environ['MONGO_COLLECTION_NAME'],
    # URL: os.environ['MONGO_DB_URL'],

    # For serverless Offline
    MONGODB: "votingdb",
    BILLSCOLLECTION: "bills",
    ISSUESCOLLECTION: "issues",
    RESULTSCOLLECTION: "results",
    USERSCOLLECTION: "users",
    VOTESCOLLECTION: "votes",
    BALLOTSPECSCOLLECTION: "ballotspecs",
    URL: "mongodb://localhost:27017/",
}

if cluster:
    ms = {
        USER: user,
        PWD: pwd,
        MONGODB: "votingdb",
        BILLSCOLLECTION: "bills",
        ISSUESCOLLECTION: "issues",
        RESULTSCOLLECTION: "results",
        USERSCOLLECTION: "users",
        VOTESCOLLECTION: "votes",
        BALLOTSPECSCOLLECTION: "ballotspecs",
        URL: 'mongodb+srv://'+user+':'+pwd+'@cluster0-ctiil.mongodb.net/votingdb?retryWrites=true&w=majority' 

    }


mongosettings = ms
