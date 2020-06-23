import datetime

import requests
from termcolor import colored


# https://hackersandslackers.com/extract-data-from-complex-json-python/
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


#
# References:https://wiki.infinidat.com/display/public/SUP/Fixing+Heartbeat+Missing+Alerts+In+Inventory
# 1: sys_hb_time  SY HB alert after 49 hours/ freq 24 hrs   NO_HEARTBEAT_RECEIVED
# 2: sa_hb_time   SA HB alert after 8 days / freq 1 week      NO_SA_HEARTBEAT_RECEIVED
# 3: rss_time     SA Keepalive RSS (Remote Support Keepalive) NO_REMOTE_SUPPORT_# KEEPALIVE_RECEIVED alert after 24 hours / freq 4 hrs
# 4:              System Keepalive _SYSTEM_KEEPALIVE_RECEIVED alert after 12 hours / freq 4 hrs


# setup stuff
mytoken = 'tpuyyTJpfj1N'
headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}

sys_url = "https://inventory.infinidat.com/api/rest/systems/"
alert_url = "https://inventory.infinidat.com/api/rest/alerts/"

##################################################################################
site_url = "https://inventory.infinidat.com/api/rest/customers/site/"
site_params = "fields=name,system_set,name&account_name=eq:British Telecom"

r_sn = requests.get(site_url, headers=headers, params=site_params)
data = r_sn.json()

for i in data['result']:

    site_name = i['name']
    serial = i['system_set']
    rss_alert = 0

    # Now we get a piece of data from each site and its serial

    for sn in serial:
        ##########################  Hostname ,model         #########################################

        host_params = "fields=serial_number,model,name&serial_number=eq:" + str(sn)
        host_url = "https://inventory.infinidat.com/api/rest/systems/"

        r_host = requests.get(host_url, headers=headers, params=host_params)
        r_host_data = r_host.json()
        hostname = r_host_data["result"][0]["name"]
        model = r_host_data["result"][0]["model"]
        #############################################################################################

        ##########################  SA and System Heartbeat ######################
        sa_sys_params = "serial_number=eq:" + str(sn) + "&fields=last_heartbeat_at,last_sa_heartbeat_at"
        sa_sys_url = "https://inventory.infinidat.com/api/rest/systems"

        sa_sys = requests.get(sa_sys_url, headers=headers, params=sa_sys_params)
        sa_sys_data = sa_sys.json()

        # First get System Heartbeat
        sys_hb_time = sa_sys_data["result"][0]["last_heartbeat_at"]
        if sys_hb_time is None:
            sys_hb_time = "None"
        else:
            sys_hb_time = datetime.datetime.strptime(sa_sys_data["result"][0]["last_heartbeat_at"],
                                                     "%Y-%m-%dT%H:%M:%SZ")
            sys_hb_time = sys_hb_time.strftime("%Y-%m-%d %H:%M")

        sa_hb_time = sa_sys_data["result"][0]["last_sa_heartbeat_at"]
        if sa_hb_time is None:
            sa_hb_time = "none"
        else:
            sa_hb_time = datetime.datetime.strptime(sa_sys_data["result"][0]["last_sa_heartbeat_at"],
                                                    "%Y-%m-%dT%H:%M:%SZ")
            sa_hb_time = sa_hb_time.strftime("%Y-%m-%d %H:%M")

        ########################## Remote Support Keepalive ######################
        eventtoken = '3aawHwNmByea'
        event_headers = {'X-API-Token': eventtoken, 'Accept-Encoding': 'identity'}

        # We have to adjust the keepalive search to look back three days as it takes to long
        # It alerts after 24 hour of no keepalive heartbeat anyway so 3 days is enough.
        today = datetime.date.today()
        start_search_date = (today - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
        # print(start_search_date)
        # datetime.today().strftime('%Y-%m-%d')

        rss_params = "system_serial=eq:" + str(
            sn) + "&timestamp=gt:" + start_search_date + "&page_size=100&code=like:_REMOTE_SUPPORT_KEEPALIVE"
        rss_url = "https://event-store-01.aws.infinidat.com/api/rest/events/"

        rss = requests.get(rss_url, headers=event_headers, params=rss_params)
        rss_data = rss.json()
        # We need to find the highest timestamp in the output. timestamp is an epoch number, so
        # (1) get all timestamps
        # (2) whichever is the highest - convert it.

        if len(rss_data["result"]) == 0:
            rss_time = "None"
            rss_alert = 1
        else:
            timestamp = extract_values(rss_data, 'timestamp')
            # print(timestamp)
            latest_timestamp = str(max(timestamp))
            # print(str(latest_timestamp))
            rss_time = datetime.datetime.fromtimestamp(int(latest_timestamp[:10])).strftime("%Y-%m-%d %H:%M")

            #  Find the difference between now and the alert time, if greater thane alert period set text red
            x = datetime.datetime.now()
            y = datetime.datetime.fromtimestamp(int(latest_timestamp[:10]))
            z = x - y
            if z.seconds > 14400:
                rss_alert = 1
                # print(rss_alert)
            else:
                rss_alert = 0

        ##########################  Output Results Here     #########################################
        if rss_alert == 1:
            p_rss_time = colored('Remote Keep: ' + str(rss_time), 'red')
        else:
            p_rss_time = str('Remote Keep: ' + str(rss_time))

        print('{:7}' '{:6}' '{:30}' '{:27}' '{:25}' '{:25}' '{}'
              .format(model,
                      str(sn),
                      hostname + " ",
                      site_name,
                      "Sy_HB: " + str(sys_hb_time),
                      "Sa_HB: " + str(sa_hb_time),
                      p_rss_time
                      ))
