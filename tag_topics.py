import requests
from operator import itemgetter

# Topics 
citizens = ["Education","Skills","Employment","Health", "Veterans", "youth","sports","Social","Indigenous","Disability"]
nature = ["Agriculture","water","Environment"]
national_development = ["Industry", "Science","Resources","Energy","Infrastructure","Transport","Regional Development","Industrial"]
borders = ["Trade","Home","Defence","Foreign","Immigration","Citizenship","Migrant"]
economy = ["Treasury", "Finance"]
communications = ["Communications"]

topics = {
    "citizens":citizens,
    "nature":nature,
    "national_development":national_development,
    "borders":borders,
    "economy":economy,
    "communications":communications,
}

# related terms 
rt = open("related_terms.csv","r")
topic_lines = rt.readlines()
headings = topic_lines.pop(0)
headings_list = headings.replace("\n","").lower().split(",")

topic_models = {}
for i in range(len(headings.replace("\n","").split(","))):
    terms = []
    for tl in topic_lines:
        term = tl.replace("\n","").split(",")[i]
        if term != "":
            terms.append(term.lower())
    topic_models[headings_list[i]] = terms


def tag_bill(bill):
    t = []
    if "portfolio" in bill.keys():
        if bill["portfolio"] != "":
            portfoilo = bill["portfolio"]
            for topic in topics.keys():
                for domain in topics[topic]:
                    if domain.lower() in portfoilo.lower():
                        if topic not in t:
                            t.append(topic)
    if t != []:
        return(t)
    else:
        p = []
        for h in headings_list:
            for rt in topic_models[h]:
                if rt in bill["short_title"].lower() or rt in bill["summary"].lower():
                    if h not in p:
                        p.append(h)
        return(p)
                
