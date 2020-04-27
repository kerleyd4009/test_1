import json
import requests
import ijson

# setup stuff
mytoken='tpuyyTJpfj1N'
headers=headers={'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}


site_url = "https://inventory.infinidat.com/api/rest/customers/site/"
site_params = "fields=name,system_set,name&account_name=eq:British Telecom"

r_sn=requests.get( site_url , headers=headers, params=site_params)
data=r_sn.json()
#print(data)

for i in data['result']:
       print(i['name'] , i['system_set'])