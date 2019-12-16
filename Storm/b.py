a=[
  {
    'servicename': 'rsConnectService-import',
    'type': 'spout',
    'id': 'entityappmanage-migrate-reader',
    'error': 'java.lang.RuntimeException: java.lang.IllegalStateException: This consumer has already been closed.\\n\tat org.apache.storm.utils.DisruptorQueue.consumeBatchToCursor(DisruptorQueue.java:522)\\n\tat org.apac'
  },
  {
    'servicename': 'entityAppService',
    'type': 'spout',
    'id': 'entityappmanage-reader',
    'error': 'java.lang.RuntimeException: java.lang.IllegalStateException: This consumer has already been closed.\\n\tat org.apache.storm.utils.DisruptorQueue.consumeBatchToCursor(DisruptorQueue.java:522)\\n\tat org.apac'
  },
  {
    'servicename': 'entityManageService',
    'type': 'spout',
    'id': 'entitymanage-largeobject-reader',
    'error': 'java.lang.RuntimeException: java.lang.IllegalStateException: This consumer has already been closed.\\n\tat org.apache.storm.utils.DisruptorQueue.consumeBatchToCursor(DisruptorQueue.java:522)\\n\tat org.apac'
  },
  {
    'servicename': 'entityManageService',
    'type': 'spout',
    'id': 'entitymanage-migrate-reader',
    'error': 'java.lang.RuntimeException: java.lang.IllegalStateException: This consumer has already been closed.\\n\tat org.apache.storm.utils.DisruptorQueue.consumeBatchToCursor(DisruptorQueue.java:522)\\n\tat org.apac'
  }
]

restarted_services=[]

for i in a:
    if 'rsConnectService' in i['servicename']:
        print(i['servicename'])