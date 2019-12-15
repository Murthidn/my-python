try:
    import sys
    import traceback
    import json
    import os
    import re
    from datetime import datetime
    from datetime import timedelta
    import utilscommon as uc
    import loadmodules
    import requests
    import time
    import traceback
    from influxdb import InfluxDBClient
except Exception as error:
    print(error)
    sys.exit(201)
try:
    imp_json_body=[]
    utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json_tmp = [{
        "measurement": 'integration_import2',
        "tags": {
            "tenant": 'rdwengg-az-dev2',
            "profile": 'sys_import_data_json_ui_task_base-2',
            "taskType": "ENTITY_IMPORT"
        },
        "time": utc_time,
        "fields": {

            "import": 10
        }
    }
    ]
    imp_json_body.extend(json_tmp)

    uc.insert_to_influx(imp_json_body, 'app_metrics')

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
