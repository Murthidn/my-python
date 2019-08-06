import json

try:
    import sys
    import loadmodules
    import requests
except Exception as error:
    print(error)
    sys.exit(201)

HEADERS = {"db": "sensu", "q": "SELECT * FROM \"alert_count\" " }
getURL="http://influxdb:8186/query?pretty=true --data-urlencode --data-urlencode"

TIMEOUT = 60  # sec
try:
    #response = requests.get(getURL, HEADERS, timeout=TIMEOUT)

    jsonresponse = json.dumps(requests.get(getURL, HEADERS, timeout=TIMEOUT).json())

    print(jsonresponse)

except requests.exceptions.Timeout:
    print('request timed out (', TIMEOUT, 'sec) <br>')
    sys.exit(2)
except requests.exceptions.RequestException as e:
    print('Error fetching data:', str(e))
    sys.exit(2)
