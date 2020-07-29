import argparse
from datetime import datetime, date
import datetime

import requests

parser = argparse.ArgumentParser(description="General Information")
parser.add_argument('-s', '--serial', type=int, dest='serialnum', nargs="*", default='0',
                    help='You must specify an account "-a" when specifying  a serial "-s" or mutiple serials')
parser.add_argument('-a', '--account', dest='account', default="Britisih Telecom",
                    help='Please enclose account names with space with double quotes')
args = parser.parse_args()




def FindAccount(serial):
    # https://inventory.infinidat.com/api/rest/systems/?serial_number=eq:1164&fields=account
    snum = serial

    ##########################  Hostname ,model         #########################################
    host_params = "fields=account&serial_number=eq:" + str(snum)
    host_url = "https://inventory.infinidat.com/api/rest/systems/"

    r_host = requests.get(host_url, headers=headers, params=host_params)
    r_host_data = r_host.json()
    # print(flatten(r_host_data))
    accountName = r_host_data['result'][0]['account']['name']

    return accountName


def ShowEvent(serial):
    # ?code=eq:INTERNAL_CUSTOM_INFO_EVENT&description=eq:SA%20Hardware%20Collector&system_serial=eq:1164
    #

    my_event_token = '3aawHwNmByea'
    event_headers = headers = {'X-API-Token': my_event_token, 'Accept-Encoding': 'identity'}
    event_url = "https://event-store-02.aws.infinidat.com/api/rest/events/"
    event_params = "system_serial=eq:" + str(
        serial) + "&code=eq:INTERNAL_CUSTOM_INFO_EVENT&description=eq:SA%20Hardware%20Collector&sort=-timestamp"
    # Here we sort descending, thus is important this means array [0] is the latest.

    events = requests.get(event_url, headers=event_headers, params=event_params)
    data = events.json()

    try:
        sas_hba_monitor = data['result'][0]['parsed_data']['data']['features']['sa_utils_monitor']['sas_hba_monitor']
    except:
        sas_hba_monitor = "Empty"

    try:
        blocked_drives_monitor = data['result'][0]['parsed_data']['data']['features']['blocked-drives-monitor'][
            'enabled']
    except:
        blocked_drives_monitor = "Empty"

    try:
        timestamp = data['result'][0]['timestamp']
        timestamp = str(timestamp)
        mytime = datetime.datetime.fromtimestamp(int(timestamp[:10])).strftime('%Y-%m-%d')
    except:
        mytime = "Empty"

    try:
        sa_utils_ver = data['result'][0]['parsed_data']['data']['versions']['sa_utils']
    except:
        sa_utils_ver = "Empty"

    return mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver


def ShowInfo(site_name, serial):
    snum = serial

    ##########################  Hostname ,model         #########################################
    host_params = "fields=serial_number,model,name&serial_number=eq:" + str(snum)
    host_url = "https://inventory.infinidat.com/api/rest/systems/"

    r_host = requests.get(host_url, headers=headers, params=host_params)
    r_host_data = r_host.json()
    hostname = r_host_data["result"][0]["name"]
    model = r_host_data["result"][0]["model"]
    #############################################################################################

    contacts_url = "https://inventory.infinidat.com/api/rest/systems/" + str(snum) + "/contacts/"

    contacts = requests.get(contacts_url, headers=headers)
    contacts_data = contacts.json()

    contact_name = contacts_data["result"]["Emergency"][0]["name"]
    contact_email = contacts_data["result"]["Emergency"][0]["email"]

    return model, snum, hostname, site_name, contact_name, contact_email


##########################   Main Program   #######################################################
# setup stuff
mytoken = 'tpuyyTJpfj1N'
headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}

sys_url = "https://inventory.infinidat.com/api/rest/systems/"
alert_url = "https://inventory.infinidat.com/api/rest/alerts/"

##################################################################################
site_url = "https://inventory.infinidat.com/api/rest/customers/site/"
site_params = "fields=name,system_set,name&account_name=eq:" + args.account

r_sn = requests.get(site_url, headers=headers, params=site_params)
data = r_sn.json()
##################  Get all the serials for an account  ##########################
mySite_Arrays = {}

for i in data['result']:
    site_name = i['name']
    serial = i['system_set']
    mySite_Arrays[site_name] = serial
##################################################################################
if args.serialnum != 0:

    for masers in args.serialnum:
        mysite_name = FindAccount(masers)
        model, sn, hostname, site_name, contact_name, contact_email = ShowInfo(mysite_name, masers)
        mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver = ShowEvent(masers)

        print('{:7}' '{:8}' '{:23}' '{:30}' '{:18}' '{:15}' "SAS MON: "'{}'  "   BLK DRV: " '{}'
              .format(model,
                      str(sn),
                      hostname + " ",
                      site_name,
                      mytime,
                      sa_utils_ver,
                      sas_hba_monitor,
                      blocked_drives_monitor))
else:
    for site_name, serial in mySite_Arrays.items():
        if len(site_name) <= 0:
            next()
        else:
            for mysn in serial:
                model, sn, hostname, site_name, contact_name, contact_email = ShowInfo(site_name, mysn)
                mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver = ShowEvent(mysn)

                print('{:7}' '{:8}' '{:23}' '{:30}' '{:18}' '{:15}' "SAS MON: "'{}'  "   BLK DRV: " '{}'
                      .format(model,
                              str(sn),
                              hostname + " ",
                              site_name,
                              mytime,
                              sa_utils_ver,
                              sas_hba_monitor,
                              blocked_drives_monitor))
