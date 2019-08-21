try:
    print('importing packages')
    import sys
    import traceback
    import loadmodules
    import json
    from datetime import datetime
    import utilscommon as uc

except Exception as error:
    print(error)
    sys.exit(201)

try:
    print('imported packages')

    measurement = 'wcf_healthcheck_data'
    utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json_body = [{
        "measurement": measurement,
        "tags": {
            "tenant": 'test'
        },
        "time": utc_time,
        "fields": {
            "host": 'testHost',
            "status": 1
        }
    }]
    uc.insert_to_influx(json_body)

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
