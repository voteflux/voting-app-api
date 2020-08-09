# voting-app-api

**We are currently running the shitchain, so please check out that branch**

## Getting started

### On first time

```
sudo apt-get install nodejs

sudo apt-get install curl software-properties-common

curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -

sudo npm install -g serverless
```

[Install MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/#install-mongodb-community-edition)

Install requirements

```
pip3 install -r requirements.txt
npm install
```

### On every startup

### Dev (offlline)

Start MongoDB

```
sudo systemctl start mongod
```

Populate/update the DB

```
python3 update_bills_db.py
python3 update_issues_db.py
python3 update_ballotspecs_db.py
python3 update_results_db.py
```

'python3 update_bills_db.py' _may be run on loop every few hours to update DB_

we haven't got a good way to update the issues collection yet

Run serverless offline

```
serverless offline
```

Ctrl+C to stop _serverless offline_

### Deploy

Add mongoDB creds to env vars:

```
MONGO_DB_USER=
MONGO_DB_PASS=
```

Populate DB

```
python3 update_bills_db.py
python3 update_issues_db.py
python3 update_ballotspecs_db.py
python3 update_results_db.py
```

May also need to check the url in `mode.py`.

Add aws creds:

```
aws configure
```

Deploy to aws:


```
serverless deploy
```

## Public Contracts


AWS Dev:

```
endpoints:
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/bill/{id}
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/bill
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/issue/{id}
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/issue
  POST - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/issue
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/result/{id}
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/result
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/spec/{id}
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/spec
```

#### Issues

To Create a new Issue, `POST` to:

```
https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/issue
```

with example body:

```json
{"token":"YOURTOKENHERE",
   "data": {"chamber": "Public",
            "short_title": "Independent Anti-corruption Commsion",
            "start_date": "2019-05-01",
            "end_date": "2020-05-30",
            "question": "Should an independent Federal ICAC be created?",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
            "sponsor": "Freedom Lobby Group"}}
```

#### Shitchain (Depreciated!)


**Depreciated** (For you @bazmatic ):


```
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/shitchain/{id}
  GET - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/shitchain
  POST - https://1j56c60pb0.execute-api.ap-southeast-2.amazonaws.com/dev/shitchain
```


Where `{id}` is the bill/issue id

To make a vote, `POST` to:

```
http://localhost:3000/dev/shitchain/
```

with example body:

```json
{
   "pub_key":"lafksdjfnhc934y8q5pcn98xpc5ny85y410c5mp9xnyv",
   "ballot_id": "r6434",
   "ballotspec_hash": "86d9935a4fcdd7d517293229527ace224287cb6ba2d07115f4784db16fece5af",
   "constituency": "Australia",
   "vote": "no"
 }
```