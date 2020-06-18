import json
import requests
import ijson


# setup stuff
mytoken = 'tpuyyTJpfj1N'
headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}

sys_url = "https://inventory.infinidat.com/api/rest/systems/"
alert_url = "https://inventory.infinidat.com/api/rest/alerts/"

##################################################################################
site_url = "https://inventory.infinidat.com/api/rest/customers/site/"
site_params = "fields=name,system_set,name&account_name=eq:British Telecom"


# Derivco, Capgemini, Pulsant and Brightsolid
#site_params = "fields=name,system_set,name&account_name=like:Capgemini"

#####################  Lets get the percs type and firmware   #################

perc_url = "https://inventory.infinidat.com/api/rest/components/perc/"
perc_params = "fields=system_serial,parent_index,firmware,type&page_size=9000"

perc_data = requests.get(perc_url, headers=headers, params=perc_params)
r_perc_data = perc_data.json()

# print(r_perc_data)
##################################################################################
r_sn = requests.get(site_url, headers=headers, params=site_params)
data = r_sn.json()

for i in data['result']:

    site_name = i['name']
    serial = i['system_set']
    # Now we get a piece of data from each site and its serial

    for sn in serial:
        perc_info = []
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
        for perc in r_perc_data['result']:
            if sn == perc['system_serial']:
                for number in range(0, 4):
                    if int(perc['parent_index']) == number:
                        perc_info.append(str(perc['parent_index']))
                        perc_info.append(str(perc['type']))
                        perc_info.append(str(perc['firmware']))
                        # perc_info.append(str(perc['system_serial']))
        perc_info_str = ' '.join(perc_info)
        #############################################################################################

        ##########################  Output Results Here     #########################################
        print('{:7}' '{:8}' '{:12}' '{:30}' '{:15}' '{:45}'
              .format(model,
                      str(sn),
                      str(version),
                      hostname + " ",
                      site_name,
                      perc_info_str))
