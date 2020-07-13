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

# Print the header for the list
print('{:7}' '{:8}' '{:30}' '{:30}' '{:15}' '{}'
      .format("Model",
              "Serial",
              "hostname" + " ",
              "site name",
              "version",
              "sa_utils_version"
              ))



for i in data['result']:

    site_name = i['name']
    serial = i['system_set']
    # Now we get a piece of data from each site and its serial

    #
    #  Code for SAS Watchdog is 5.0.0.0.239
    #

    for sn in serial:
        ##########################  Hostname ,model         #########################################
        host_params = "fields=serial_number,model,version,name&serial_number=eq:" + str(sn)
        host_url = "https://inventory.infinidat.com/api/rest/systems/"

        r_host = requests.get(host_url, headers=headers, params=host_params)
        r_host_data = r_host.json()
        hostname = r_host_data["result"][0]["name"]
        model = r_host_data["result"][0]["model"]
        version = r_host_data["result"][0]["version"]
        #############################################################################################

        ##########################  Enter New Extraction (example below) Here ######################
        sa_params = "system_serial=eq:" + str(sn) + "&fields=firmware,ttk_version,rsa_version,hw_collector_version," \
                                                    "sa_utils_version,recovery_tools "
        sa_url = "https://inventory.infinidat.com/api/rest/components/supportappliance/"

        sa_info = requests.get(sa_url, headers=headers, params=sa_params)
        sa_info_data = sa_info.json()

        sa_rsa_version = sa_info_data['result'][0]['rsa_version']
        sa_firmware = sa_info_data['result'][0]['firmware']
        sa_ttk_version = sa_info_data['result'][0]['ttk_version']
        sa_hw_collector_version = sa_info_data['result'][0]['hw_collector_version']
        sa_utils_version = sa_info_data['result'][0]['sa_utils_version']
        # sa_recovery_tools = sa_info_data['result'][0]['recovery_tools']
        #############################################################################################

        ##########################  Output Results Here     #########################################
        print('{:7}' '{:8}' '{:30}' '{:30}' '{:15}' '{}'
              .format(model,
                      str(sn),
                      hostname,
                      site_name,
                      version,
                      sa_utils_version
                      ))
