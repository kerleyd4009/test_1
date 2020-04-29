import json
import requests
import ijson

# setup stuff
mytoken = 'tpuyyTJpfj1N'
headers = headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}
bats = {}

sys_url = "https://inventory.infinidat.com/api/rest/systems/"
alert_url = "https://inventory.infinidat.com/api/rest/alerts/"
# site_params_alert_against = "system=eq:$abox&fields=component,code"


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
        site_params_bat = "system_serial=eq:" + str(sn)
        bat_node_url = "https://inventory.infinidat.com/api/rest/components/upsbattery/"

        ups_node_bat = requests.get(bat_node_url, headers=headers, params=site_params_bat)
        bat_data = ups_node_bat.json()

        for indx in range(0, 3):
             parent_index = bat_data["result"][indx]["parent_index"]
             vendor = bat_data["result"][indx]["vendor"]
             battery_date = bat_data["result"][indx]["battery_date"]
             bats[indx] = (parent_index, vendor, battery_date)

        # node_drv_failures = len(node_drv_data['result'])
        #############################################################################################

        ##########################  Output Results Here     #########################################


        print('{:7}' '{:8}' '{:30}' '{:30}' '{}' \
              .format(model, \
                      str(sn), \
                      "UPS"+str(bats[0][0]) + " " + str(bats[0][1]) + " "+ " " + str(bats[0][2]) + "   "+\
                      "UPS"+str(bats[1][0]) + " " + str(bats[1][1]) + " "+ " " + str(bats[1][2]) + "   "+\
                      "UPS"+str(bats[2][0]) + " " + str(bats[2][1]) + " "+ " " + str(bats[2][2]) + "   ",\
                      hostname + " ", \
                      site_name))
