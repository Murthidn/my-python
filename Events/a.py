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
    exp_json_body=[]


    utc_time = '2019-12-15T13:15:31Z'
    json_tmp = [{
        "measurement": 'integration_export',
        "tags": {
            "tenant": 'rdwengg-az-dev2',
            "profile": 'Acenda_Variant_Scheduled_Publi-2',
            "taskType": "ENTITY_EXPORT"
        },
        "time": utc_time,
        "fields": {

            "export": 10
        }
    }
    ]
    exp_json_body.extend(json_tmp)

    uc.insert_to_influx(exp_json_body, 'app_metrics')

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
