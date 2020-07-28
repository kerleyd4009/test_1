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

        ##########################  Enter New Extraction (example below) Here ######################
        # site_params_node_drv = "system_serial=eq:" + str(sn) + "&state=ne:OK&state=ne:UNCONFIGURED"
        # event_url_local_drv = "https://inventory.infinidat.com/api/rest/components/localdrive/"

        # r_node_drv = requests.get(event_url_local_drv, headers=headers, params=site_params_node_drv)
        # node_drv_data = r_node_drv.json()
        # node_drv_failures = len(node_drv_data['result'])
        #############################################################################################

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
                print(site_name)
                #ShowInfo(site_name, mysn)


else:
    for site_name, serial in mySite_Arrays.items():
        ShowInfo(site_name, serial)
