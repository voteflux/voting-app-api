import os

USER = 'user'
PWD = 'pwd'
MONGODB = 'mongodb'
MONGOCOLLECTION = 'mongocollection'
URL = 'url'

prod = True

ms = {
    MONGODB: os.environ['MONGO_DB_NAME'],
    MONGOCOLLECTION: os.environ['MONGO_COLLECTION_NAME'],
    URL: os.environ['MONGO_DB_URL'],
}

if prod:
    ms = {
        USER: os.environ['MONGO_DB_USER'],
        PWD: os.environ['MONGO_DB_PASS'],
        MONGODB: os.environ['MONGO_DB_NAME'],
        MONGOCOLLECTION: os.environ['MONGO_COLLECTION_NAME'],
        URL: "mongodb+srv://" + usr + ":" + pwd + "@" +
        os.environ['MONGO_DB_URL'] + "/test?retryWrites=true&w=majority"
    }


mongosettings = ms
