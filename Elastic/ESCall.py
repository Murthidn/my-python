import sys
import loadmodules
import requests

def callAPI(url):
    timeout=10
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.Timeout as e:
        return False
    except requests.exceptions.RequestException as e:
        return False
    else:
        if r.status_code == 200:
            return r

url = 'http://elasticsearch1:9200/_cat/nodes?v'

a = callAPI(url)
print(a.request)