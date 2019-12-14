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
    TIMEOUT = 60  # sec
    timeinterval = 5  # minutes
    tenants = []
    json_body = []
    env = os.environ['envname']
    measurement_name = 'integrationReport2'
    utc_time_from = (datetime.utcnow() - timedelta(minutes=int(timeinterval))).strftime("%Y-%m-%dT%H:%M:00.000-0000")


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


    # Get list of tenants
    url = ('http://rdp-rest:8085/dataplatform/api/configurationservice/get')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-rdp-userId': 'system_user',
               'x-rdp-userRoles': '["admin"]'}
    tenantQuery = {'params': {'query': {'filters': {'typesCriterion': ['tenantserviceconfig']}}}}
    rt = requesthelper(url, tenantQuery, headers, TIMEOUT)

    for item in rt.json()['response']['configObjects']:
        tenants.append(item['id'])


    def getCountFromResponse(json_dict):
        count = json_dict.get('response').get('totalRecords')
        return count


    for x in tenants:
        importProfiles = []
        exportProfiles = []
        tenant = str(x)
        taskIdList = list()

        # Get External Events
        query = {"params": {"query": {"filters": {"typesCriterion": ["externalevent"], "propertiesCriterion": [
            {"createdDate": {"gt": str(utc_time_from), "type": "_DATETIME"}}], "attributesCriterion": [
            {"profileType": {"exact": "ENTITY_IMPORT"}}]}}, "fields": {"attributes": ["taskId"]}}}
        url = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        response = requesthelper(url, query, headers, TIMEOUT)

        # Get Task IDs
        if not response.json()['response']['totalRecords'] == 0:
            totalRec = response.json()['response']['totalRecords']
            for i in range(totalRec):
                taskId = response.json()['response']['events'][i]['data']['attributes']['taskId']['values'][0]['value']
                if taskId not in taskIdList:
                    taskIdList.append(taskId)

            for i in taskIdList:
                # Get Task Summary
                query = {"params": {"query": {"filters": {"typesCriterion": ["tasksummaryobject"],
                                                          "attributesCriterion": [{"taskId": {"exact": i}},
                                                                                  {"status": {"exact": "Completed"}}]}},
                                    "fields": {"attributes": ["totalRecords", "profileName", "totalRecordsSuccess",
                                                              "totalRecordsCreate", "totalRecordsUpdate",
                                                              "totalRecordsDelete"]}}}
                url = ('http://rdp-rest:8085/' + tenant + '/api/requesttrackingservice/get')
                response = requesthelper(url, query, headers, TIMEOUT)
                if not response.json()['response']['totalRecords'] == 0:
                    totalImport = response.json()['response']['requestObjects'][0]['data']['attributes']['totalRecords']['values'][0]['value']
                    totalSuccessImport = response.json()['response']['requestObjects'][0]['data']['attributes']['totalRecordsSuccess']['values'][0]['value']
                    profileName = response.json()['response']['requestObjects'][0]['data']['attributes']['profileName']['values'][0]['value']
                    create = response.json()['response']['requestObjects'][0]['data']['attributes']['totalRecordsSuccess']['values'][0]['value']
                    update = response.json()['response']['requestObjects'][0]['data']['attributes']['totalRecordsUpdate']['values'][0]['value']
                    delete = response.json()['response']['requestObjects'][0]['data']['attributes']['totalRecordsDelete']['values'][0]['value']
                    submittedBy = response.json()['response']['requestObjects'][0]['data']['attributes']['submittedBy']['values'][0]['value']

                    # Get Total External Events
                    query = {"params": {"query": {"filters": {"typesCriterion": ["externalevent"],
                                                              "attributesCriterion": [{"taskId": {"exact": i}}]}},
                                        "options": {"maxRecords": 1}}}
                    url = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
                    response = requesthelper(url, query, headers, TIMEOUT)
                    json_dict = json.loads(response.text)
                    externalEvents = getCountFromResponse(json_dict)

                    # Get Total Manage Events
                    query = {"params": {"query": {"filters": {"typesCriterion": ["entitymanageevent"],
                                                              "attributesCriterion": [{"taskId": {"exact": i}}]}},
                                        "options": {"maxRecords": 1}}}
                    url = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
                    response = requesthelper(url, query, headers, TIMEOUT)
                    json_dict = json.loads(response.text)
                    manageEvents = getCountFromResponse(json_dict)

                    # Get Total Govern Events
                    query = {"params": {"query": {"filters": {"typesCriterion": ["entitygovernevent"],
                                                              "attributesCriterion": [{"taskId": {"exact": i}}]}},
                                        "options": {"maxRecords": 1}}}
                    url = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
                    response = requesthelper(url, query, headers, TIMEOUT)
                    json_dict = json.loads(response.text)
                    governEvents = getCountFromResponse(json_dict)

                    # Get Total Request Objects
                    query = {"params": {"query": {"filters": {"typesCriterion": ["requestobject"],
                                                              "attributesCriterion": [{"taskId": {"exact": i}}]}},
                                        "options": {"maxRecords": 1}}}
                    url = ('http://rdp-rest:8085/' + tenant + '/api/requesttrackingservice/get')
                    response = requesthelper(url, query, headers, TIMEOUT)
                    json_dict = json.loads(response.text)
                    requestObjects = getCountFromResponse(json_dict)

                    utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    json_tmp = [{
                        "measurement": measurement_name,
                        "tags": {
                            "envname": env,
                            "tenant": tenant,
                            "profileName": profileName,
                            "taskType": "ENTITY_IMPORT"
                        },
                        "time": utc_time,
                        "fields": {
                            "user":submittedBy,
                            "taskId": str(i),
                            "import": totalImport,
                            "success": totalSuccessImport,
                            "create": create,
                            "update": update,
                            "delete": delete,
                            "externalEvents": externalEvents,
                            "manageEvents": manageEvents,
                            "governEvents": governEvents,
                            "requestObjects": requestObjects
                        }
                    }
                    ]
                    json_body.extend(json_tmp)
    uc.insert_to_influx(json_body, 'app_metrics')

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
