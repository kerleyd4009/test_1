import json
import requests
import ijson


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
        print('{:7}' '{:8}' '{:30}' '{:30}'
              .format(model,
                      str(sn),
                      hostname + " ",
                      site_name))

        ##########################  Enter New Extraction (example below) Here ######################

        ssd_params = "system_serial=eq:" + str(
            sn) + "&fields=system_serial,index,parent_index,vendor,model,serial_number,wearout"
        ssd_url = "https://inventory.infinidat.com/api/rest/components/localdrive/"
        ssd_node = requests.get(ssd_url, headers=headers, params=ssd_params)
        ssd_drv_data = ssd_node.json()['result']

        for myi in ssd_drv_data:
            this_ssd_name = "N" + str(myi['parent_index']) + "D" + str(myi['index'])
            ssd_serial_number = str(myi['serial_number'])
            print(str(sn),"   ",myi['wearout'], myi['vendor'], myi['model'],this_ssd_name, ssd_serial_number)

            #print('{:6}' '{:9}' '{:30}' '{:20}' '{}' '{}'
            #      .format(myi['wearout'],
            #              myi['vendor'],
            #              myi['model'],
            #              str(this_ssd_name),
            #              str(myi['serial_number'] or "None"),
            #              ))

        #############################################################################################

        ############        ##########################  Output Results Here     #########################################
        ##############  Output Results Here     #########################################
