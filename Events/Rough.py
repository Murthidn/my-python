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
    exp_json_body=[]
    utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json_tmp = [{
        "measurement": 'integration_import2',
        "tags": {
            "envname": 'engg-az-dev2',
            "tenant": 'rdwengg-az-dev2',
            "taskType": "ENTITY_IMPORT"
        },
        "time": utc_time,
        "fields": {
            "user": 'rdwadmin@riversand.com',
            "profile": 'sys_import_data_json_ui_task_base-1',
            "taskId": ' a3e2dc74-e08e-4fcb-8382-99d462c0dce3-3',
            "import": 10,
            "create": 10,
            "update": 10,
            "delete": 10,
            "attempt": 1,
            "externalEvents": 5,
            "manageEvents": 5,
            "governEvents": 5,
            "requestObjects": 5
        }
    }
    ]
    imp_json_body.extend(json_tmp)


    utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json_tmp = [{
        "measurement": 'integration_export2',
        "tags": {
            "envname": 'engg-az-dev2',
            "tenant": 'rdwengg-az-dev2',
            "taskType": "ENTITY_EXPORT"
        },
        "time": utc_time,
        "fields": {
            "user": 'system_user',
            "profile": 'Acenda_Variant_Scheduled_Publi-1',
            "taskId": '36a6cafb-9d73-40d8-bdbe-978dcd6366b9-2',
            "export": 10,
            "attempt": 1,
            "externalEvents": 5
        }
    }
    ]
    exp_json_body.extend(json_tmp)

    uc.insert_to_influx(imp_json_body, 'app_metrics')
    uc.insert_to_influx(exp_json_body, 'app_metrics')

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
