try:
    import sys
    import os

    sys.path.insert(0, '/usr/python-packages/dn-requests/')
    import requests

    import pathlib
    from shutil import copyfile

except Exception as error:
    print(error)
    sys.exit(201)

HOME = '/root'
DOMAIN = None
TOKEN = None

# REST API Access
def clientRequest(getURL, getHeaders):
    TIMEOUT = 60  # sec
    try:
        response = requests.get(getURL, headers=getHeaders, timeout=TIMEOUT)

    except requests.exceptions.Timeout:
        print('request timed out (', TIMEOUT, 'sec) <br>')
        sys.exit(2)

    except requests.exceptions.RequestException as e:
        print('Error fetching data:', str(e))
        sys.exit(2)

    return response


def getNetrcFile(location, subscription):

    netrc_filename='.netrc_'+location

    if subscription == 'RS-Violet-Prod' or subscription == 'RS-Violet-Non-Prod':
        netrc_filename=netrc_filename+"_india"
    else:
        netrc_filename=netrc_filename+"_us"

    if subscription.find("Non-Prod") == -1:
        netrc_filename = netrc_filename +"_prod"
    else:
        netrc_filename = netrc_filename +"_non-prod"

    file = pathlib.Path(HOME+'/'+netrc_filename)
    if file.exists():
        for root, dirs, files in os.walk(HOME):
            if netrc_filename in files:
                src = os.path.join(root, netrc_filename)
                copyfile(src, '/etc/sensu/plugins/.netrc')
    else:
        print("Sensu is not configured to handle "+location+" region. Please contact DevOps team to configure Databricks automation for this region.")
        sys.exit(201)

def getDatabricksTokenFromNetrcFile():
    file = open('/etc/sensu/plugins/.netrc')

    for line in file:
        if line.strip():
            fields = line.strip().split()
            if fields[1].endswith('@riversand.com'):
                continue

            elif fields[1].endswith('.azuredatabricks.net'):
                continue

            else:
                return fields[1]
        else:
            continue

def getAzureRegionName():
    METADATA_URL = 'http://169.254.169.254/metadata/instance?api-version=2017-08-01'
    METADATA_HEADERS = {'Metadata': 'true'}
    getMetaData = clientRequest(METADATA_URL, METADATA_HEADERS)

    if getMetaData.status_code == 200 and 'compute' in getMetaData.json() and 'location' in getMetaData.json()['compute']:
        return getMetaData.json()['compute']['location']

    else:
        print("Error while fetching metadata")