try:
    import sys
except Exception as error:
    print(error)
    sys.exit(201)
sys.path.insert(0, '/usr/python-packages/dn-docker/')
sys.path.insert(0, '/usr/python-packages/dn-influxdb/')
sys.path.insert(0, '/usr/python-packages/dn-requests/')
sys.path.insert(0, '/usr/python-packages/dn-interruptingcow/')
sys.path.insert(0, '/usr/python-packages/dn-numpy/')
sys.path.insert(0, '/usr/python-packages/dn-azure/')
sys.path.insert(0, '/usr/python-packages/dn-azure-monitor/')
sys.path.insert(0, '/usr/python-packages/dn-azure-keyvault/')
sys.path.insert(0, '/usr/python-packages/dn-pika/')
sys.path.insert(0, '/usr/python-packages/dn-confluent-kafka/')
sys.path.insert(0, '/usr/python-packages/dn-jira/')
sys.path.insert(0, '/usr/python-packages/dn-adal/')
sys.path.insert(0, '/usr/python-packages/dn-kafka-python/')
