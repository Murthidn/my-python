import sys
import os
import pathlib
from shutil import copyfile

DOMAIN = None
TOKEN = None
HOME = '/etc/sensu/plugins'

def getAuth(location, subscription):

    netrc_filename='.netrc_'+location

    if subscription == 'RS-Violet-Prod' or subscription == 'RS-Violet-Non-Prod':
        netrc_filename=netrc_filename+"_india"
    else:
        netrc_filename=netrc_filename+"_us"

    if subscription.find("Non-Prod") == -1:
        netrc_filename = netrc_filename +"_prod"
    else:
        netrc_filename = netrc_filename +"_non-prod"

    file = pathlib.Path(HOME+"/helpers/"+netrc_filename)
    if file.exists():
        for root, dirs, files in os.walk(HOME+'/helpers'):
            if netrc_filename in files:
                src = os.path.join(root, netrc_filename)
                copyfile(src, HOME+'/.netrc')
    else:
        print("File not exist")
        sys.exit(201)

location='eastus'
subscription='Riversand Violet - Non-Production'
getAuth(location, subscription)

file = open(HOME+'/.netrc')

for line in file:
    if line.strip():
        fields = line.strip().split()
        if fields[1] == 'token':
            continue

        elif fields[1].endswith('.azuredatabricks.net'):
            DOMAIN = fields[1]

        else:
            TOKEN = fields[1]
    else:
        continue

print(DOMAIN)
print(TOKEN)