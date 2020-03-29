from bill.create import create
import json

print(create({"body": json.dumps(
    {
        "s8769": "Kip",
        "r2342": "Bill2"
    }
)}, None))
