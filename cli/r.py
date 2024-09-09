import requests
import json
import datetime

mod_id= 'P7dR8mSH'
response = requests.get(f'https://api.modrinth.com/v2/project/{mod_id}/version')
json_data = json.loads(response.text)

version = "1.21.1"
temp = ""
most_recent_v={}

for r in json_data:
  if r['game_versions'][0] == version and r['version_type'] == "release":
    if temp != "":
      if datetime.date(int(temp.split("-")[0]), int(temp.split("-")[1]), int(temp.split("-")[2])) < \
        datetime.date(int(r['date_published'].split('T')[0].split("-")[0]), int(r['date_published'].split('T')[0].split("-")[1]), int(r['date_published'].split('T')[0].split("-")[2])):
        temp=r['date_published']
        temp = temp.split("T")[0]
        most_recent_v=r
    else:
      temp=r['date_published']
      temp = temp.split("T")[0]
      most_recent_v=r

print(r)
