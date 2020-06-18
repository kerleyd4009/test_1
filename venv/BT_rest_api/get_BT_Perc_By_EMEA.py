import json
import requests
import ijson

mytoken = 'tpuyyTJpfj1N'
headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}

########################   Here we get all the EMEA Sales sn  ##############
sales_url = "https://inventory.infinidat.com/api/rest/systems/"
sales_param = "sales_region=eq:EMEA&fields=serial_number&page_size=9000"

r_sales = requests.get(sales_url, headers=headers, params=sales_param)
r_sales_data = r_sales.json()

###############################################################################

site_url = "https://inventory.infinidat.com/api/rest/systems/"
site_params = "fields=serial_number,site,account,model,version,name&page_size=9000"

site_data = requests.get(site_url, headers=headers, params=site_params)
r_site_data = site_data.json()

# print(r_site_data)

#####################  Lets get the percs type and firmware   #################

perc_url = "https://inventory.infinidat.com/api/rest/components/perc/"
perc_params = "fields=system_serial,parent_index,firmware,type&page_size=9000"

perc_data = requests.get(perc_url, headers=headers, params=perc_params)
r_perc_data = perc_data.json()

# print(r_perc_data)
##################################################################################


######################  TA info  ###################################################
TA_url = "https://inventory.infinidat.com/api/rest/contacts/contactsystems/"
TA_params = "role=eq:TA&order=1&fields=system,contact.name,contact.email&page_size=9000"

r_TA_data = requests.get(TA_url, headers=headers, params=TA_params)
TA_data = r_TA_data.json()

# print(TA_data)

####################################################################################


for sn in r_sales_data['result']:
    site_info = []
    perc_info = []
    ta_info = ""

    for perc in r_perc_data['result']:
        if sn['serial_number'] == perc['system_serial']:
            for number in range(0, 4):
                if int(perc['parent_index']) == number:
                    perc_info.append(str(perc['parent_index']))
                    perc_info.append(str(perc['type']))
                    perc_info.append(str(perc['firmware']))
                    # perc_info.append(str(perc['system_serial']))

    for site in r_site_data['result']:
        if sn['serial_number'] == site['serial_number']:
            site_info = (str(sn['serial_number']),
                         str(site['model']),
                         str(site['version']),
                         str(site['name']),
                         str(site['account']['name']),
                         str(site['account']['country_name']
                             ))

    for ta in TA_data['result']:
        if sn['serial_number'] == ta['system']:
            ta_info = ta['contact.name']
            # print(sn, str(perc_info), str(site_info), str(ta_info) + "\n")

    psite_info = ','.join(site_info)
    pperc_info = ','.join(perc_info)

    #####################  Publish  #########################################################
    print(psite_info + "," + str(ta_info) + "," + pperc_info)

    filename = 'tmp/EMEA_PERC_Info.csv'
    with open(filename, 'a') as f:
        f.write(psite_info + "," + str(ta_info) + "," + pperc_info + "\n")
