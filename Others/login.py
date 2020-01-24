import os

envName= 'engg-az-dev2' #input('Enter env name:')
pemKeyPath='/home/murthi/Videos/Softwares/Keys/PEM/'

envList={
    'engg-az-dev2':'us-azure-non-prod.pem'
}

envMgrIp={
    'engg-az-dev2':'40.80.150.19'
}

os.system('ssh -i'+ pemKeyPath+envList.get(envName)+ ' ubuntu@'+ envMgrIp.get(envName)+ ' -p 50000')
