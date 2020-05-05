import json
import requests
import ijson
import time
from datetime import datetime
import re

# setup stuff
this_serial =""
mytoken = 'tpuyyTJpfj1N'
headers = headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}

sys_url = "https://inventory.infinidat.com/api/rest/systems/"
site_url = "https://inventory.infinidat.com/api/rest/customers/site/"
site_params = "fields=name,system_set,name&account_name=eq:British Telecom"

r_sn = requests.get(site_url, headers=headers, params=site_params)
data = r_sn.json()
# print(data)
for i in data['result']:

    site_name = i['name']
    short_site_name = (site_name[:12])
    serial = i['system_set']
    # Now we get a piece of data from each site and its serial

    for sn in serial:


        timefrom = "T00:00"
        my_event_token = '3aawHwNmByea'
        event_headers = headers = {'X-API-Token': my_event_token, 'Accept-Encoding': 'identity'}
        event_url = "https://event-store-01.aws.infinidat.com/api/rest/events_metadata/"
        event_params = "timestamp=gt:2020-05-05" + timefrom + "&system_serial=eq:" + str(sn)

        events = requests.get(event_url, headers=event_headers, params=event_params)
        data = events.json()

        for iev in data['result']:


            descrp = iev['description']
            level = iev['level']
            code = iev['code']

            timestamp = str(iev['timestamp'])
            time = datetime.fromtimestamp(int(timestamp[:10]))
            # print(time)
            p = re.compile('HARD', re.IGNORECASE)
            m = p.search(code)
            if m:
                if this_serial != sn:
                    print("\n")

                print('{:6}''{:15}' '{:23}' '{:25}' '{:8}' '{}'.format(str(sn), short_site_name, str(time), code, level,
                                                                       descrp))
                this_serial = sn