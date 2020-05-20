import getopt
import sys
import json
import requests
from datetime import date, datetime

serial = ""
account = ""


def usage():
    print("Usage: " + sys.argv[0] + "[OPTIONS")
    print("\t--serial\txxxxxxx")
    print("\t--account\tSome Company")

    print("Example")
    print("=======")
    print("get_BT_TEMP_events_serial_option.py -s 1162")
    print("get_BT_TEMP_events_serial_option.py -a British Telecom\n")
    sys.exit(1)


try:
    opts, args = getopt.getopt(sys.argv[1:], "s:a:h", ["serial=", "account=", "help"])
except getopt.error as err:
    # Output error, and return with an error code
    print(str(err))
    sys.exit(2)

for o, a in opts:

    if o in ("-s", "--serial"):
        serial = a
    elif o in ("-a", "--account"):
        account = a
    elif o in ("-h", "--help"):
        usage()
        sys.exit()

argc = len(sys.argv)
if argc == 1:
    serial = "1465"
    account = "British  Telecom"

#print("Serial Entered: " + str(serial) + "\n")
#print("Account Entered: " + account)
#######################################################################################################################
# setup stuff
mytoken = '3aawHwNmByea'
headers = headers = {'X-API-Token': mytoken, 'Accept-Encoding': 'identity'}

temp_url = "https://event-store-01.aws.infinidat.com/api/rest/events_metadata/"
temp_params = "system_serial=eq:" + str(serial) + "&description=like:temperature&fields=timestamp,description&page_size=1000"

t_alert = requests.get(temp_url, headers=headers, params=temp_params)
t_alert_data = t_alert.json()


for iev in t_alert_data['result']:
    descrp = iev['description']
    timestamp = str(iev['timestamp'])
    time = datetime.fromtimestamp(int(timestamp[:10])).strftime('%d/%m %H:%M:%S')

    print('{:20}' '{:8}' .format(time, descrp ))
