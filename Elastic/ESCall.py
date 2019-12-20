import sys
import loadmodules
import requests
import json


def requesthelper(url, query, headers, timeout):
    try:
        tenant = requests.post(url, data=json.dumps(query), headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        print('<br>request timed out (', timeout, 'sec)')
        sys.exit(201)
    except requests.exceptions.RequestException as e:
        print('<br>exception encountered:', str(e))
        sys.exit(201)
    else:
        return tenant

url = 'http://elasticsearch1:9200/rdwengg-az-dev2entityindex_v8/_search'
headers = {'Content-type': 'application/json'}
query = { "query": { "terms": { "_id": ["fd9ThcZhTUGbCR6XP42FGQ"] } } }
data = requesthelper(url, query, headers, 60)
print(data.json())