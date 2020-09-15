from datetime import date, datetime
import re
import requests

# setup stuff
this_serial = ""

''' "code": "CUSTOM_WARNING_EVENT",
            "description": "System Ambient temperature level is WARNING, front temperature is 31.33, back temperature is 40.67",
            "id": 243873,
            "level": "WARNING",
            "pk": 236905790,  <<<<<<<<<<<   gives the full detail
            "reporter": "PLATFORM",
            "seq_num": 98979,
            "system_serial": 1461,
            "system_version": "4.0.40.120",
            "timestamp": 1599157008289.0,
            "visibility": "CUSTOMER"
        }'''

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
        # Here we get all the events for today from 00:00
        today = date.today()
        timefrom = "T00:00"

        my_event_token = '3aawHwNmByea'
        event_headers = headers = {'X-API-Token': my_event_token, 'Accept-Encoding': 'identity'}
        event_url = "https://event-store-01.aws.infinidat.com/api/rest/events_metadata/"
        # event_params = "timestamp=gt:" + str(today) + timefrom + "&system_serial=eq:" + str(sn) +
        # "&code=like:CUSTOM_WARNING_EVENT"
        event_params = "system_serial=eq:" + str(sn) + "&code=eq:CUSTOM_WARNING_EVENT"

        events = requests.get(event_url, headers=event_headers, params=event_params)
        data = events.json()

        for iev in data['result']:
            descrp = iev['description']
            level = iev['level']
            code = iev['code']
            seq_num = str(iev['seq_num'])

            timestamp = str(iev['timestamp'])
            time = datetime.fromtimestamp(int(timestamp[:10])).strftime('%d/%m/%Y %H:%M')

        # Look for all these events
        p = re.compile('temperature', re.IGNORECASE)
        m = p.search(descrp)

        if m:
            print('{:5}''{:14}' '{:18}' '{:12}' '{}'.format(str(sn),
                                                            short_site_name[:12],
                                                            time,
                                                            level,
                                                            descrp))

    this_serial = sn
