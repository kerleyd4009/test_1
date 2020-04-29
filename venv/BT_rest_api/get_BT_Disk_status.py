import json
import requests
import ijson

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
mytoken='tpuyyTJpfj1N'
headers=headers={'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}



sys_url = "https://inventory.infinidat.com/api/rest/systems/"
alert_url = "https://inventory.infinidat.com/api/rest/alerts/"
#site_params_alert_against = "system=eq:$abox&fields=component,code"


##################################################################################
site_url = "https://inventory.infinidat.com/api/rest/customers/site/"
site_params = "fields=name,system_set,name&account_name=eq:British Telecom"

r_sn=requests.get( site_url , headers=headers, params=site_params)
data=r_sn.json()


for i in data['result']:

       site_name = i['name']
       serial = i['system_set']
       # Now we get a piece of data from each site and its serial

       for sn in serial:
              ########################## Local Drive Failures ###########################################
              site_params_node_drv = "system_serial=eq:" + str(sn) + "&state=ne:OK&state=ne:UNCONFIGURED"
              event_url_local_drv = "https://inventory.infinidat.com/api/rest/components/localdrive/"

              r_node_drv = requests.get(event_url_local_drv, headers=headers, params=site_params_node_drv)
              node_drv_data = r_node_drv.json()
              node_drv_failures = len(node_drv_data['result'])
              #############################################################################################

              ########################## Enclosure Drive Failures ##########################################
              site_params_encl_drv = "sort=parent_index&system_serial=eq:" + str(sn) + "&state=ne:ACTIVE"
              event_url_encl_drv = "https://inventory.infinidat.com/api/rest/components/enclosuredrive/"

              r_encl_drv = requests.get(event_url_encl_drv, headers=headers, params=site_params_encl_drv)
              encl_drv_data = r_encl_drv.json()
              encl_failures= len(encl_drv_data['result'])
              #############################################################################################

              ##########################  Hostname ,model         ##########################################
              host_params="fields=serial_number,model,name&serial_number=eq:" + str(sn)
              host_url="https://inventory.infinidat.com/api/rest/systems/"

              r_host=requests.get(host_url, headers=headers, params=host_params)
              r_host_data=r_host.json()
              hostname = r_host_data["result"][0]["name"]
              model = r_host_data["result"][0]["model"]
              #############################################################################################

              ##########################   Event   ########################################################
              alert_comp_params= "fields=component,code&system=eq:" + str(sn)
              alert_comp_url="https://inventory.infinidat.com/api/rest/alerts/"

              r_alert = requests.get(alert_comp_url, headers=headers, params=alert_comp_params)
              r_alert_data = r_alert.json()
              #print(r_alert_data)

              comp = ' '.join(extract_values(r_alert_data, "component"))

              code = ' '.join(extract_values(r_alert_data, "code"))
              code = code.replace("ENCLOSURE_DRIVE_INACTIVE", "")

              #print(comp, code)

              #############################################################################################

              print('{:7}' '{:8}' '{:12}' '{:15}' '{:30}' '{:12}' '{:6}' '{}'\
                      .format(model,\
                               str(sn),\
                               "Node hdd:" + str(node_drv_failures),\
                               "Encl hdd: " + str(encl_failures),\
                               hostname + " ",\
                               site_name + " ",\
                               comp + " ",\
                               code))