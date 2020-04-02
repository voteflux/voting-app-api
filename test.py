from user.create import create
from bill.get import get
import json

print(create({"body": json.dumps(
    {"First Name": "Bob", "Last Name": "Katter", "Age": 58, "Sex": "M", "Location": "Sydney"}
)}, None))


print(get({"pathParameters":
           {
               "id": ""
           }}, None))
