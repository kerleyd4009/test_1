import json
import requests
import ijson
import datetime

#
# References:https://wiki.infinidat.com/display/public/SUP/Fixing+Heartbeat+Missing+Alerts+In+Inventory
# 1: sys_hb_time  IBOX HB alert after 49 hours/ freq 24 hrs   NO_HEARTBEAT_RECEIVED
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

        rss_params = "system_serial=eq:" + str(sn) + "&code=like:_REMOTE_SUPPORT_KEEPALIVE"
        rss_url = "https://event-store-01.aws.infinidat.com/api/rest/events/"

        rss = requests.get(rss_url, headers=event_headers, params=rss_params)
        rss_data = rss.json()

        if len(rss_data["result"]) == 0:
            rss_time = "None"
        else:
            rss_keep = str(rss_data["result"][0]["timestamp"])
            rss_time = datetime.datetime.fromtimestamp(int(rss_keep[:10])).strftime("%Y-%m-%d %H:%M")



    ##########################  Output Results Here     #########################################
        print('{:7}' '{:8}' '{:30}' '{:27}' '{:30}' '{:30}' '{}'
          .format(model,
                  str(sn),
                  hostname + " ",
                  site_name,
                  "Sy_HB: " + str(sys_hb_time),
                  "Sa_HB: " + str(sa_hb_time),
                  "RSS Tun: " + str(rss_time)

                  ))
