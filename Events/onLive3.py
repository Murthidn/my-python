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
    def requesthelper(url, query ,headers,timeout):
        try:
            rt = requests.post(url, data=json.dumps(query), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            print ('<br>request timed out (', TIMEOUT, 'sec)')
            sys.exit(201)
        except requests.exceptions.RequestException as e:
            print ('<br>exception encountered:', str(e))
            sys.exit(201)
        else:
            return rt

    def getTaskSummary(taskSummaryObj, type):
        taskSummaryData={}
        taskSummaryData['taskAttemptCount'] = 0
        if type == 'import' or type == 'export':
            taskSummaryData['profileName']= taskSummaryObj['profileName']['values'][0]['value']
            taskSummaryData['userId']= taskSummaryObj['userId']['values'][0]['value']
            taskSummaryData['taskId']= taskSummaryObj['taskId']['values'][0]['value']
            taskSummaryData['totalRecordsSuccess']= taskSummaryObj['totalRecordsSuccess']['values'][0]['value']
            if 'taskAttemptCount' in taskSummaryObj:
                taskSummaryData['taskAttemptCount'] = taskSummaryObj['taskAttemptCount']['values'][0]['value']

        if type == 'import':
            taskSummaryData['totalRecordsCreate']= taskSummaryObj['totalRecordsCreate']['values'][0]['value']
            taskSummaryData['totalRecordsUpdate']= taskSummaryObj['totalRecordsUpdate']['values'][0]['value']
            taskSummaryData['totalRecordsDelete']= taskSummaryObj['totalRecordsDelete']['values'][0]['value']
        return taskSummaryData

    def getTotalExternalEvents(taskId, tenant):
        externalEventsUrl = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        externalEventsQuery = { "params": { "query": { "filters": { "typesCriterion": [ "externalevent" ], "attributesCriterion": [ { "taskId": { "exact": taskId } } ] } }, "options": { "maxRecords": 1 } } }
        externalEventsResponse = requesthelper(externalEventsUrl, externalEventsQuery, headers, TIMEOUT)
        return externalEventsResponse.json()['response']['totalRecords']

    def getTotalManageEvents(taskId, tenant):
        manageEventsUrl = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        manageEventsQuery = { "params": { "query": { "filters": { "typesCriterion": [ "entitymanageevent" ], "attributesCriterion": [ { "taskId": { "exact": taskId } } ] } }, "options": { "maxRecords": 1 } } }
        manageEventsResponse = requesthelper(manageEventsUrl, manageEventsQuery, headers, TIMEOUT)
        return manageEventsResponse.json()['response']['totalRecords']

    def getTotalGovernEvents(taskId, tenant):
        governEventsUrl = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        governEventsQuery = { "params": { "query": { "filters": { "typesCriterion": [ "entitygovernevent" ], "attributesCriterion": [ { "taskId": { "exact": taskId } } ] } }, "options": { "maxRecords": 1 } } }
        governEventsResponse = requesthelper(governEventsUrl, governEventsQuery, headers, TIMEOUT)
        return governEventsResponse.json()['response']['totalRecords']

    def getTotalRequestObjects(taskId, tenant):
        requestObjectUrl = ('http://rdp-rest:8085/' + tenant + '/api/requesttrackingservice/get')
        requestObjectQuery = { "params": { "query": { "filters": { "typesCriterion": [ "requestobject" ], "attributesCriterion": [ { "taskId": { "exact": taskId } } ] } }, "options": { "maxRecords": 1 } } }
        requestObjectResponse = requesthelper(requestObjectUrl, requestObjectQuery, headers, TIMEOUT)
        return requestObjectResponse.json()['response']['totalRecords']

    TIMEOUT = 60 #sec
    timeinterval = 200 #min
    tenants = []
    imp_json_body = []
    exp_json_body = []
    env = os.environ['envname']
    imp_measurement = 'integration_import'
    exp_measurement = 'integration_export'

    utc_time_from = (datetime.utcnow() - timedelta(minutes=int(timeinterval))).strftime("%Y-%m-%dT%H:%M:00.000-0000")

    #Get ALl Tenants
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-rdp-userId': 'system_user', 'x-rdp-userRoles': '["admin"]'}
    tenantGetUrl = ('http://rdp-rest:8085/dataplatform/api/configurationservice/get')
    tenantGetQuery = {'params': {'query': {'filters': {'typesCriterion': ['tenantserviceconfig']}}}}
    tenantGetResponse = requesthelper(tenantGetUrl, tenantGetQuery, headers, TIMEOUT)

    for item in tenantGetResponse.json()['response']['configObjects']:
        tenants.append(item['id'])

    for t in tenants:
        #Get Import Task Summary
        taskSummaryUrl=('http://rdp-rest:8085/'+ str(t) +'/api/requesttrackingservice/get')
        importTaskSummaryQuery={ "params": { "query": { "filters": { "typesCriterion": [ "tasksummaryobject" ], "propertiesCriterion": [ { "createdDate": { "gt": str(utc_time_from), "type": "_DATETIME" } } ], "attributesCriterion": [ { "taskType": { "exact": "ENTITY_IMPORT" } }, { "status": { "exact": "Completed" } } ] } }, "fields": { "attributes": [ "profileName", "userId", "taskId", "totalRecordsSuccess", "totalRecordsCreate", "totalRecordsUpdate", "totalRecordsDelete", "taskAttemptCount" ] } } }
        importTaskSummaryQueryResponse = requesthelper(taskSummaryUrl, importTaskSummaryQuery, headers, TIMEOUT)
        if not importTaskSummaryQueryResponse.json()['response']['totalRecords']==0:
            totalImportTaskSummary=importTaskSummaryQueryResponse.json()['response']['totalRecords']
            for i in range(totalImportTaskSummary):
                importTaskSummary = getTaskSummary(importTaskSummaryQueryResponse.json()['response']['requestObjects'][i]['data']['attributes'], 'import')
                totalExternalEvents=getTotalExternalEvents(importTaskSummary['taskId'], str(t))
                totalManageEvents=getTotalManageEvents(importTaskSummary['taskId'], str(t))
                totalGovernEvents=getTotalGovernEvents(importTaskSummary['taskId'], str(t))
                totalRequestObjects=getTotalRequestObjects(importTaskSummary['taskId'], str(t))

                utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                json_tmp = [{
                    "measurement": imp_measurement,
                    "tags": {
                        "envname": env,
                        "tenant": str(t),
                        "taskType": "ENTITY_IMPORT"
                    },
                    "time": utc_time,
                    "fields": {
                        "user": importTaskSummary['userId'],
                        "profile": importTaskSummary['profileName'],
                        "taskId": importTaskSummary['taskId'],
                        "import": importTaskSummary['totalRecordsSuccess'],
                        "create": importTaskSummary['totalRecordsCreate'],
                        "update": importTaskSummary['totalRecordsUpdate'],
                        "delete": importTaskSummary['totalRecordsDelete'],
                        "attempt": importTaskSummary['taskAttemptCount'],
                        "externalEvents": totalExternalEvents,
                        "manageEvents": totalManageEvents,
                        "governEvents": totalGovernEvents,
                        "requestObjects": totalRequestObjects
                    }
                }
                ]
                imp_json_body.extend(json_tmp)

        #Get Export Task Summary
        exportTaskSummaryQuery={ "params": { "query": { "filters": { "typesCriterion": [ "tasksummaryobject" ], "propertiesCriterion": [ { "createdDate": { "gt": str(utc_time_from), "type": "_DATETIME" } } ], "attributesCriterion": [ { "taskType": { "exact": "ENTITY_EXPORT" } }, { "status": { "exact": "Completed" } } ] } }, "fields": { "attributes": [ "profileName", "userId", "taskId", "totalRecordsSuccess", "totalRecordsCreate", "totalRecordsUpdate", "totalRecordsDelete","taskAttemptCount" ] } } }
        exportTaskSummaryQueryResponse = requesthelper(taskSummaryUrl, exportTaskSummaryQuery, headers, TIMEOUT)
        if not exportTaskSummaryQueryResponse.json()['response']['totalRecords'] == 0:
            totalExportTaskSummary=exportTaskSummaryQueryResponse.json()['response']['totalRecords']
            for k in range(totalExportTaskSummary):
                exportTaskSummary = getTaskSummary(exportTaskSummaryQueryResponse.json()['response']['requestObjects'][k]['data']['attributes'], 'export')
                totalExternalEvents=getTotalExternalEvents(exportTaskSummary['taskId'], str(t))

                utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                json_tmp = [{
                    "measurement": exp_measurement,
                    "tags": {
                        "envname": env,
                        "tenant": str(t),
                        "taskType": "ENTITY_EXPORT"
                    },
                    "time": utc_time,
                    "fields": {
                        "user": exportTaskSummary['userId'],
                        "profile": exportTaskSummary['profileName'],
                        "taskId": exportTaskSummary['taskId'],
                        "export": exportTaskSummary['totalRecordsSuccess'],
                        "attempt": exportTaskSummary['taskAttemptCount'],
                        "externalEvents": totalExternalEvents
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
