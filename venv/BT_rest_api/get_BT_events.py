from datetime import date, datetime
import re
import requests

# setup stuff
this_serial = ""

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
        #event_params = "timestamp=gt:2020-05-05" + timefrom + "&system_serial=eq:" + str(sn)
        event_params = "timestamp=gt:" + str(today) + timefrom + "&system_serial=eq:" + str(sn)

        events = requests.get(event_url, headers=event_headers, params=event_params)
        data = events.json()

        for iev in data['result']:

            descrp = iev['description']
            level = iev['level']
            code = iev['code']
            seq_num = str(iev['seq_num'])

            timestamp = str(iev['timestamp'])
            time = datetime.fromtimestamp(int(timestamp[:10])).strftime('%H:%M')


            # Look for all these events
            p = re.compile('INFO|ERROR|CRITICAL', re.IGNORECASE)
            m = p.search(level)

            # Exclude these codes
            int_code = re.compile(
                'INTERNAL_CUSTOM_INFO_EVENT|CUSTOM|PLATFORM_INFO|INFINIMETRIC|INITIATOR|HEARTBEAT|BBU|SG|KEEPALIVE'
                '|REPLICA')
            int_code_res = int_code.search(code)

            if m and not int_code_res:

                if this_serial != sn:
                    print("\n")

                print('{:5}''{:14}' '{:10}' '{:25}' '{:8}' '{}'.format(str(sn), short_site_name[:12], time, code,
                                                                       level, descrp))
                # print('{:8}''{:15}' '{:25}' '{:8}' '{}'.format(str(sn), short_site_name,  code, level, descrp))

                this_serial = sn
