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
print('''References:https://wiki.infinidat.com/display/public/SUP/Fixing+Heartbeat+Missing+Alerts+In+Inventory 
1: SY HB   alert after 49 hours check every 24 hrs  NO_HEARTBEAT_RECEIVED     we red alert on 48 hours 
2: SA HB   alert after 8 days   check every 1 week  NO_SA_HEARTBEAT_RECEIVED  we red alert on 7 days 
3: SA->RSS alert after 24 hours check every 4 hrs   NO_REMOTE_SUPPORT_ alert  we red alert over 4 hours 
 
''')
# Need to look into this : System Keepalive _SYSTEM_KEEPALIVE_RECEIVED alert after 12 hours / freq 4 hrs


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

        ############################  SYS Heartbeat  ###############################################
        sys_hb_time = sa_sys_data["result"][0]["last_heartbeat_at"]
        if sys_hb_time is None:
            sys_hb_time = "None"
            sys_hb_time_alert = 1
        else:
            sys_hb_time = datetime.datetime.strptime(sa_sys_data["result"][0]["last_heartbeat_at"],
                                                     "%Y-%m-%dT%H:%M:%SZ")
            sys_hb_time = sys_hb_time.strftime("%Y-%m-%d %H:%M")

            sys = (datetime.datetime.now() - datetime.datetime.strptime(sys_hb_time, "%Y-%m-%d %H:%M")).total_seconds()
            if sys > 172800:
                sys_hb_time_alert = 1
                # we alert after 49hrs, so we test at 48 hours (172800 secs)
            else:
                sys_hb_time_alert = 0
        ############################  SA Heartbeat  ###############################################
        sa_hb_time = sa_sys_data["result"][0]["last_sa_heartbeat_at"]
        if sa_hb_time is None:
            sa_hb_time = "none"
            sa_hb_time_alert = 1

        else:
            sa_hb_time = datetime.datetime.strptime(sa_sys_data["result"][0]["last_sa_heartbeat_at"],
                                                    "%Y-%m-%dT%H:%M:%SZ")
            sa_hb_time = sa_hb_time.strftime("%Y-%m-%d %H:%M")

            sa = (datetime.datetime.now() - datetime.datetime.strptime(sa_hb_time, "%Y-%m-%d %H:%M")).total_seconds()
            if sa > 604800:
                sa_hb_time_alert = 1
                # we alert after 8 days, so we test at 7 days (604800 secs)

            else:
                sa_hb_time_alert = 0

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
            latest_timestamp = str(max(timestamp))
            rss_time = datetime.datetime.fromtimestamp(int(latest_timestamp[:10])).strftime("%Y-%m-%d %H:%M")

            #  Find the difference between now and the alert time, if greater thane alert period set text red
            p = (datetime.datetime.now() - datetime.datetime.fromtimestamp(int(latest_timestamp[:10]))).total_seconds()
            if p > 14400:
                rss_alert = 1
                # print(rss_alert)
            else:
                rss_alert = 0

        ##########################  Output Results Here     #########################################
        # Set the colours red here
        # We need to ignore the below as the are ruled out by BT firewall, webex and ssh key needed
        #
        # F2240        1576        dy021ifb01_21CN_RoBT
        # F2240        2750        dy021ifb02
        # F2240        1575        ap021ifb01_21CN_RoBT
        # F2240        2615        ap021ifb02_21CN_OR
        # F2240        1577        by021ifb01_21CN_RoBT
        # F2240        2902        oy021ifb02

        if rss_alert == 1 and sn in {1576, 2750, 1575, 2615, 1577, 2902}:
            p_rss_time = colored(str('SA Keep: ' + str(rss_time)) + '  Blocked BT Firewall', 'blue')
        elif rss_alert == 1:
            p_rss_time = colored(str('SA Keep: ' + str(rss_time)), 'red')
        else:
            p_rss_time = str('SA Keep: ' + str(rss_time))

        if sys_hb_time_alert == 1:
            sys_hb_time = colored(str('Sys HB: ' + str(sys_hb_time)), 'red')
        else:
            sys_hb_time = str('Sys HB: ' + str(sys_hb_time))

        if sa_hb_time_alert == 1:
            sa_hb_time = colored(str('SA HB: ' + str(sa_hb_time)), 'red')
        else:
            sa_hb_time = str('SA HB: ' + str(sa_hb_time))

        ####################################################################################################

        print('{:7}' '{:6}' '{:30}' '{:27}' '{:30}' '{:30}' '{}'
              .format(model,
                      str(sn),
                      hostname + " ",
                      site_name,
                      sys_hb_time,
                      sa_hb_time,
                      p_rss_time
                      ))
