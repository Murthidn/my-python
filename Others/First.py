import sys
sys.path.insert(0, '/usr/python-packages/dn-requests/')
import requests

getMetaData = requests.get("http://169.254.169.254/metadata/instance?api-version=2017-08-01", headers={'Metadata':'true'})

if getMetaData.status_code == 200 and 'compute' in getMetaData.json() and 'location' in getMetaData.json()['compute']:
    print("success")
    location=getMetaData.json()['compute']['location']
    DOMAIN = location+'.azuredatabricks.net'
    print(DOMAIN)


else:
    print("Fail")