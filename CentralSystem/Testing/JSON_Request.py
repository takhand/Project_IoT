import json
import requests 

url = "http://test8osman.appspot.com/post"
data = {'Destination': 'oii', 'Source': 3, 'Value': 34 }
payload = {'id':34}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
j = json.dumps(data)
r = requests.post(url, data=j, headers=headers)

print j
print type(j)
print r