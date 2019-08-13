try:
    import sys
    import traceback
    #import WCFHealthChecks.loadmodules
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
    def requesthelper(url, query, headers, timeout):
        try:
            rt = requests.post(url, data=json.dumps(query), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            print('<br>request timed out (', TIMEOUT, 'sec)')
            sys.exit(201)
        except requests.exceptions.RequestException as e:
            print('<br>exception encountered:', str(e))
            sys.exit(201)
        else:
            return rt

    TIMEOUT = 60  # sec
    exit_status = 0
    user = 'system_user'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
               'x-rdp-userId': 'system_user', 'x-rdp-userRoles': '["admin"]'}

    url = ('http://rdp-rest:8085/dataplatform/api/configurationservice/get')
    tenantQuery = {'params': {'query': {'filters': {
        'typesCriterion': ['tenantserviceconfig']}}, 'fields': {'attributes': ['_ALL']}}}
    rt = requesthelper(url, tenantQuery, headers, TIMEOUT)

    for item in rt.json()['response']['configObjects']:
        tenant = item['id']
        wcfurl = item['data']['jsonData']['services']['entityGovernService']['serviceSpecific']['workflow']['resturi']

        print(wcfurl+'/WorkflowRestService.svc')
        status = 0

        try:
            r = requests.get(wcfurl+'/WorkflowRestService.svc', timeout=10)
            #print(r.status_code)
            if r.status_code != 200:
                status=1
        except requests.ConnectionError:
            #print("failed to connect")
            status=1

        print(tenant)
        print(status)

        measurement = 'wcf_healthcheck_data'
        utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        json_body = [{
            "measurement": measurement,
            "tags": {
                "tenant": tenant
            },
            "time": utc_time,
            "fields": {
                "tenant_dummy": tenant,
                "status": status
            }
        }]
        uc.insert_to_influx(json_body)

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
