from bill.create import create
from bill.get import get
import json
from ausbills.federal_parliment import all_bills, Bill

# print(all_bills)
for i in range(len(all_bills)):
    url = all_bills[i]["URL"]
    bill = Bill(url)
    # print(bill.data)
    bill.data['Intro House'] = str(bill.data['Intro House'])
    bill.data['Passed House'] = str(bill.data['Passed House'])
    bill.data['Intro Senate'] = str(bill.data['Intro Senate'])
    bill.data['Passed Senate'] = str(bill.data['Passed Senate'])
    bill.data['Assent Date'] = str(bill.data['Assent Date'])
    bill.data['Act No'] = bill.data.pop('Act No.')
    # print(bill.data['Assent Date'])
    create({"body": json.dumps(bill.data)}, None)
