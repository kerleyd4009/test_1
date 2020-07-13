import json
import requests
import ijson
from collections import Counter


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

        ##########################  Enter New Extraction (example below) Here ######################
        encl_dd_params = "system_serial=eq:" + str(sn) + "&page_size=1000&fields=tb_capacity,vendor,model,parent_index"
        encl_dd_url = "https://inventory.infinidat.com/api/rest/components/enclosuredrive/"

        r_encl_dd = requests.get(encl_dd_url, headers=headers, params=encl_dd_params)
        encl_dd_data = r_encl_dd.json()

        encl_dd_data_model_count = len(extract_values(encl_dd_data, 'model'))
        encl_dd_data_model = extract_values(encl_dd_data, 'model')
        # print(encl_dd_data_model)
        encl_dd_data_model_uniq = set(extract_values(encl_dd_data, 'model'))
        print()
        print('{:7}' '{:8}' '{:30}' '{:15}'
              .format(model,
                      str(sn),
                      hostname + " ",
                      site_name),
              end='   ')

        for models in encl_dd_data_model_uniq:
            mycount = encl_dd_data_model.count(models)
            print('{}' '-' '{:22}'
                  .format(str(mycount),
                          str(models),
                          ), end='  ')

        #############################################################################################

        ##########################  Output Results Here     #########################################
