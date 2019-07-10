try:
    import json
    import base64
    import requests
    import sys
    import traceback
except Exception as error:
    print(error)
    sys.exit(201)

try:
    TIMEOUT = 60  # sec
    DOMAIN = 'eastus.azuredatabricks.net'
    TOKEN = b'dapi059eecaf6835aafbd02def39b82f7976'
    BASE_URL = 'https://%s/api/2.0/jobs/list' % (DOMAIN)
    headers = {"Content-Type": "application/json",
               "Authorization": b"Basic " + base64.standard_b64encode(b"token:" + TOKEN)}

    try:
        response = requests.get(BASE_URL, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            print("Success!")
        else:
            print("Error")

    except requests.exceptions.Timeout:
        print('request %s timed out (', TIMEOUT, 'sec) <br>' % (DOMAIN))
        sys.exit(2)
    except requests.exceptions.RequestException as e:
        print('Error fetching azure databricks job data:', str(e))
        sys.exit(2)


except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
