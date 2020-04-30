import json
import requests
import ijson

mytoken = 'tpuyyTJpfj1N'
headers =  {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}


##########################  Enter New Extraction (example below) Here ######################
TA_url = "https://inventory.infinidat.com/api/rest/contacts/contactsystems/"
TA_params = "role=eq:TA&order=1&fields=system,contact.name,contact.email&page_size=9000"

r_TA_data = requests.get(TA_url, headers=headers, params=TA_params)
TA_data = r_TA_data.json()
#print(TA_data)

count = 0
for ta in TA_data['result']:
        if ta['contact.name'] == 'Lee Sirett':
            print(ta['contact.name'] + " " + str(ta['system']))
            count += 1

print("Total of Lee accounts is " + str(count))
#ibox = TA_data['result'][5]['system']

#############################################################################################
#print(ibox)
##########################  Output Results Here     #########################################
#print('{:7}' '{:8}' '{:30}' '{:15}' \
#      .format(model, \
#              str(sn), \
#              hostname + " ", \
#              ibox))
