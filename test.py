from user.create import create
from bill.get import get
import json

print(create({"body": json.dumps(
    {
        "s8769": "Kip",
        "r2342": "Bill2"
    }
)}, None))


print(get({"pathParameters":
           {
               "id": "c87ace5a-70d7-11ea-8026-681729a3bf9c"
           }}, None))
