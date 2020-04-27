import json
import requests
import ijson

# setup stuff
mytoken='tpuyyTJpfj1N'
headers=headers={'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}
PARAMS = {'account_name':"British Telecom"}

url='https://inventory.infinidat.com/api/rest/systems'

r=requests.get( url , headers=headers, params=PARAMS)
data=r.json()

print ('{:20}' '{:30}' '{:30}' '{:30}' '{:30}' .format('Serial number','Site name','Uses FC','Uses iscsi','uses NAS'))

for i in data['result']:
    print('{:20}' '{:30}' '{:30}' '{:30}' '{:30}'\
    .format(str(i['serial_number']) \
           , i['site']['name'] \
           , str(i['uses_fibre_channel'])\
           , str(i['uses_iscsi']) \
           , str(i['uses_nfs'])))



