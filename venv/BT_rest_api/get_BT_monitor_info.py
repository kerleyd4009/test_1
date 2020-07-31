#
#   A script to get some inventory information and then collect
#   sas_hab_monitor and blocked_drive_monitor from the "last" ( most recent)
#   sent SA heartbeat
#
#   Provided with no copyright and at your own risk
#
#    Modified to include V3 heartbeats, stored in different place.,
#
#

# Set you inventory key
mytoken = 'tpuyyTJpfj1N'

# Set your event store key
my_event_token = '3aawHwNmByea'

##########################################################################################
# Set up the input argumenets, defaul no args to help

import argparse
import sys
from time import strftime
import requests
from datetime import datetime

####################################################################################################################
parser = argparse.ArgumentParser(description="General Information")

parser.add_argument('-s', '--serial', type=int, dest='serialnum', nargs="*", default='0',
                    help='You can specify different serials from diffrent accounts, if you like. Space separated'
                         'e.g # python mon_info.py -s 3196 1164 2590')
parser.add_argument('-a', '--account', dest='account', default="Britisih Telecom",
                    help='Please enclose account names with space with double quotes, only one account at a time'
                         'e.g   # python mon_info.py -a "Capgemini Global"')
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

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


def ShowEvent(serial,heartbeat_file):
    # ?code=eq:INTERNAL_CUSTOM_INFO_EVENT&description=eq:SA%20Hardware%20Collector&system_serial=eq:1164
    #

    # my_event_token = '3aawHwNmByea'
    event_headers = headers = {'X-API-Token': my_event_token, 'Accept-Encoding': 'identity'}
    event_url = "https://event-store-02.aws.infinidat.com/api/rest/events/"
    event_params = "system_serial=eq:" + str(
        serial) + "&code=eq:" + heartbeat_file + "&description=eq:SA%20Hardware%20Collector&sort=-timestamp"
    # Here we sort descending (-timestamp), thus is important this means array [0] is the latest.

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
        mytime = datetime.fromtimestamp(int(timestamp[:10])).strftime('%Y-%m-%d')
        
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
    host_params = "fields=serial_number,version,model,name&serial_number=eq:" + str(snum)
    host_url = "https://inventory.infinidat.com/api/rest/systems/"

    r_host = requests.get(host_url, headers=headers, params=host_params)
    r_host_data = r_host.json()

    
    hostname = r_host_data["result"][0]["name"]
    model = r_host_data["result"][0]["model"]
    version = r_host_data["result"][0]["version"]
    #############################################################################################

    contacts_url = "https://inventory.infinidat.com/api/rest/systems/" + str(snum) + "/contacts/"

    contacts = requests.get(contacts_url, headers=headers)
    contacts_data = contacts.json()

    contact_name = contacts_data["result"]["Emergency"][0]["name"]
    contact_email = contacts_data["result"]["Emergency"][0]["email"]

    return model, snum, hostname, site_name, contact_name, contact_email, version


##########################   Main Program   #######################################################
# setup stuff
# mytoken = 'tpuyyTJpfj1N'
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
        model, sn, hostname, site_name, contact_name, contact_email,version = ShowInfo(mysite_name, masers)
        if str(version[:1]) == "3":
             heartbeat_file = "CUSTOM_INFO_EVENT"
             mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver = ShowEvent(masers,heartbeat_file)
        else:
             heartbeat_file = "INTERNAL_CUSTOM_INFO_EVENT"
             mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver = ShowEvent(masers,heartbeat_file)



        print('{:6}' '{:6}' '{:12}' '{:23}' '{:30}' '{:18}' '{:15}' "SAS MON: "'{}'  "   BLK DRV: " '{:17}' '{}'
              .format(model,
                      str(sn),
                      version,
                      hostname[:27],
                      site_name[:26],
                      mytime,
                      sa_utils_ver,
                      sas_hba_monitor,
                      blocked_drives_monitor,
                      contact_email))
else:
    for site_name, serial in mySite_Arrays.items():
        if len(site_name) <= 0:
            next()
        else:

            for mysn in serial:
                model, sn, hostname, site_name, contact_name, contact_email, version = ShowInfo(site_name, mysn)

                if str(version[:1]) == "3":
                    heartbeat_file = "CUSTOM_INFO_EVENT"
                    mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver = ShowEvent(mysn,heartbeat_file)
                else:
                    heartbeat_file = "INTERNAL_CUSTOM_INFO_EVENT"
                    mytime, sas_hba_monitor, blocked_drives_monitor, sa_utils_ver = ShowEvent(mysn,heartbeat_file)

                print('{:6}' '{:6}' '{:12}' '{:29}' '{:30}' '{:12}' '{:15}' '{:17}'  '{:17}' '{}'
                      .format(model,
                              str(sn),
                              str(version),
                              hostname[:27],
                              site_name[:26],
                              mytime,
                              sa_utils_ver,
                              "SAS MON: " + str(sas_hba_monitor),
                              "BLK DRV: " + str(blocked_drives_monitor),
                              contact_email
                              ))
