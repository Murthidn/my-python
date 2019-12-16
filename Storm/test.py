try:
    import sys
    import traceback
    import loadmodules
    import os
    import json
    import requests
    from datetime import datetime
    import utilscommon as uc
except Exception as error:
    print(error)
    sys.exit(201)
try:
    measurement = 'autoHealing_upon_error2'
    utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    err = 'java.lang.RuntimeException: java.lang.IllegalStateException: This consumer has already been closed.\\n\tat org.apache.storm.utils.DisruptorQueue.consumeBatchToCursor(DisruptorQueue.java:522)\\n\tat org.apac'
    json_body = [{
        "measurement": measurement,

        "tags": {
            "servicename": "entityManageService",
            "type":"spout",
            "id":"entitymanage-reader"
        },
        "time": utc_time,
        "fields": {
            "error": err
        }
    }]
    uc.insert_to_influx(json_body, 'tech_metrics')

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
