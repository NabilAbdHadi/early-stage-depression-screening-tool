import json 

with open('Data Training.json', encoding='utf8', mode='r') as json_file:
    data = json.load(json_file)
    token = data['token text']