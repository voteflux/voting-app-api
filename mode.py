import os
import logging


config = AttrDict()


def set_config(env_key, default, from_string_f=lambda x: x, private=False):
    nonlocal config
    if env_key not in os.environ or not os.environ[env_key]:
        config[env_key] = default if not callable(default) else default()
    else:
        config[env_key] = from_string_f(os.getenv(env_key))
    if not private:
        logging.info("Set config k,v: `%s`,`%s`" % (env_key, config[env_key]))
    else:
        logging.info("Set config k,v: `%s` (private)" % (env_key,))
    if config[env_key] is None:
        raise Exception(f'set_config error: var: {env_key}, default: {default}, value: {config[env_key]}')


set_config('MONGODB_URI', 'mongodb://localhost:27017/billtracker-local-dev', private=True)

set_config('MONGO_DB_USER', None)
set_config('MONGO_DB_PASS', None, private=True)
set_config('MONGO_DB_URL', None)
set_config('MONGO_DB_NAME', None)



# These are _dict keys_, not values; values are set in `ms` below
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

# to be used as values, sometimes
user = os.environ['MONGO_DB_USER']
pwd = os.environ['MONGO_DB_PASS']
url = os.environ['MONGO_DB_URL']
ISSUE_TOKEN = os.environ['ISSUE_CREATE_TOKEN']


# print(user, url, pwd)
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
    URL: "localhost:27017",
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
        URL: "mongodb+srv://" + user + ":" + pwd + "@" +
        url + "/test?retryWrites=true&w=majority"
    }


ms.update(config=config)

mongosettings = ms
