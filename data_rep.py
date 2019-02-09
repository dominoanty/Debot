import json
from pprint import pprint

with open('human\\22206388.json') as data_file:    
    data = json.load(data_file)

for data_item in data:
    print(repr(data_item["text"]))