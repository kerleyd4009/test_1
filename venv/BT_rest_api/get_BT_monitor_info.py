import json
import parser

import requests
import requests
import ijson
import argparse

parser = argparse.ArgumentParser(description="General Information")
parser.add_argument('-s', '--serial', type=int, dest='serialnum', nargs="*", default='0',
                    help='You must specify an account "-a" when specifying  a serial "-s" ')
parser.add_argument('-a', '--account', dest='account', default='British Telecom',
                    help='Please enclose account names with space with double quotes')
args = parser.parse_args()


def flatten(d, sep="///"):
    import collections

    obj = collections.OrderedDict()

    def recurse(t, parent_key=""):

        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)

    return obj


##########################  This func pulls all the keys in a json output    ####################
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


def ShowEvent(serial):
    # ?code=eq:INTERNAL_CUSTOM_INFO_EVENT&description=eq:SA%20Hardware%20Collector&system_serial=eq:1164
    #
    my_event_token = '3aawHwNmByea'
    event_headers = headers = {'X-API-Token': my_event_token, 'Accept-Encoding': 'identity'}
    event_url = "https://event-store-02.aws.infinidat.com/api/rest/events/"
    event_params = "system_serial=eq:" + str(serial) + "&code=eq:INTERNAL_CUSTOM_INFO_EVENT&description=eq:SA%20Hardware%20Collector"

    events = requests.get(event_url, headers=event_headers, params=event_params)

    data = events.json()
    # print(data)
    # print(flatten(data))
    sas_hba_monitor = data['result'][4]['parsed_data']['data']['features']['sa_utils_monitor']['sas_hba_monitor']
    blocked_drives_monitor = data['result'][4]['parsed_data']['data']['features']['blocked-drives-monitor']['enabled']
    print("SAS HBA Monitor ", sas_hba_monitor)
    print("Blocked Drive Monitor ", blocked_drives_monitor)

    # ('result///4///parsed_data///data///features///sa_utils_monitor///sas_hba_monitor', True)
    # ('result///4///parsed_data///data///features///blocked-drives-monitor///enabled', True)


def ShowInfo(site_name, serial):
    for sn in serial:
        ##########################  Hostname ,model         #########################################
        host_params = "fields=serial_number,model,name&serial_number=eq:" + str(sn)
        host_url = "https://inventory.infinidat.com/api/rest/systems/"

        r_host = requests.get(host_url, headers=headers, params=host_params)
        r_host_data = r_host.json()
        hostname = r_host_data["result"][0]["name"]
        model = r_host_data["result"][0]["model"]
        #############################################################################################

        contacts_url = "https://inventory.infinidat.com/api/rest/systems/" + str(sn) + "/contacts/"

        contacts = requests.get(contacts_url, headers=headers)
        contacts_data = contacts.json()

        contact_name = contacts_data["result"]["Emergency"][0]["name"]
        contact_email = contacts_data["result"]["Emergency"][0]["email"]

        ##########################  Output Results Here     #########################################

        print('{:7}' '{:8}' '{:30}' '{:30}' '{:28}' "email: " '{}'
              .format(model,
                      str(sn),
                      hostname + " ",
                      site_name,
                      contact_name,
                      contact_email))


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

mySite_Arrays = {}

for i in data['result']:
    site_name = i['name']
    serial = i['system_set']
    mySite_Arrays[site_name] = serial

if args.serialnum != 0:

    for masers in args.serialnum:
        for site_name, serial in mySite_Arrays.items():
            if masers in serial:
                mysn = [masers]
                ShowInfo(site_name, mysn)
                ShowEvent(masers)
                # masers is a int
                # mysn is a list of masers


else:
    for site_name, serial in mySite_Arrays.items():
        ShowInfo(site_name, serial)
