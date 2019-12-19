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

    def getTotalExternalEvents(taskId, tenant):
        externalEventsUrl = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        externalEventsQuery = {"params": {"query": { "filters": {"typesCriterion": ["externalevent"], "attributesCriterion": [{"taskId": {"exact": taskId}}]}}, "options": {"maxRecords": 1}}}
        externalEventsResponse = requesthelper(externalEventsUrl, externalEventsQuery, headers, TIMEOUT)
        return externalEventsResponse.json()['response']['totalRecords']


    def getTotalManageEvents(taskId, tenant):
        manageEventsUrl = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        manageEventsQuery = {"params": {"query": {"filters": {"typesCriterion": ["entitymanageevent"], "attributesCriterion": [{"taskId": {"exact": taskId}}]}}, "options": {"maxRecords": 1}}}
        manageEventsResponse = requesthelper(manageEventsUrl, manageEventsQuery, headers, TIMEOUT)
        return manageEventsResponse.json()['response']['totalRecords']


    def getTotalGovernEvents(taskId, tenant):
        governEventsUrl = ('http://rdp-rest:8085/' + tenant + '/api/eventservice/get')
        governEventsQuery = {"params": {"query": {"filters": {"typesCriterion": ["entitygovernevent"], "attributesCriterion": [{"taskId": {"exact": taskId}}]}}, "options": {"maxRecords": 1}}}
        governEventsResponse = requesthelper(governEventsUrl, governEventsQuery, headers, TIMEOUT)
        return governEventsResponse.json()['response']['totalRecords']


    def getTotalRequestObjects(taskId, tenant):
        requestObjectUrl = ('http://rdp-rest:8085/' + tenant + '/api/requesttrackingservice/get')
        requestObjectQuery = {"params": {"query": { "filters": {"typesCriterion": ["requestobject"], "attributesCriterion": [{"taskId": {"exact": taskId}}]}}, "options": {"maxRecords": 1}}}
        requestObjectResponse = requesthelper(requestObjectUrl, requestObjectQuery, headers, TIMEOUT)
        return requestObjectResponse.json()['response']['totalRecords']

    #Start Point
    TIMEOUT = 60  # sec
    timeinterval = 60  # min
    tenants = []
    json_body = []
    env = os.environ['envname']
    measurement = 'integration_report'
    utc_time_from = (datetime.utcnow() - timedelta(minutes=int(timeinterval))).strftime("%Y-%m-%dT%H:%M:00.000-0000")

    # Get ALl Tenants
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-rdp-userId': 'system_user', 'x-rdp-userRoles': '["admin"]'}
    tenantGetUrl = ('http://rdp-rest:8085/dataplatform/api/configurationservice/get')
    tenantGetQuery = {'params': {'query': {'filters': {'typesCriterion': ['tenantserviceconfig']}}}}
    tenantGetResponse = requesthelper(tenantGetUrl, tenantGetQuery, headers, TIMEOUT)

    for item in tenantGetResponse.json()['response']['configObjects']:
        tenants.append(item['id'])

    taskSummaryQuery = { "params": { "query": { "filters": { "typesCriterion": [ "tasksummaryobject" ], "propertiesCriterion": [ { "createdDate": { "gt": str(utc_time_from), "type": "_DATETIME" } } ], "attributesCriterion": [ { "taskType": { "exacts": [ "ENTITY_IMPORT", "ENTITY_EXPORT" ] } }, { "status": { "exact": "Processing", "not": "true" } } ] } }, "fields": { "attributes": [ "_ALL" ] } } }

    for t in tenants:
        taskSummaryUrl = ('http://rdp-rest:8085/' + str(t) + '/api/requesttrackingservice/get')
        taskSummaryAPIResponse = requesthelper(taskSummaryUrl, taskSummaryQuery, headers, TIMEOUT)
        if not taskSummaryAPIResponse.json()['response']['totalRecords'] == 0:
            totalTaskSummary = taskSummaryAPIResponse.json()['response']['totalRecords']
            for i in range(totalTaskSummary):
                taskSummaryData = {}
                taskSummaryObj = taskSummaryAPIResponse.json()['response']['requestObjects'][i]['data']['attributes']
                taskSummaryData['taskAttemptCount'] = 0
                taskSummaryData['userId'] = taskSummaryObj['userId']['values'][0]['value']
                taskSummaryData['profileName'] = taskSummaryObj['profileName']['values'][0]['value']
                taskSummaryData['taskId'] = taskSummaryObj['taskId']['values'][0]['value']
                taskSummaryData['taskType'] = taskSummaryObj['taskType']['values'][0]['value']
                taskSummaryData['status'] = taskSummaryObj['status']['values'][0]['value']
                taskSummaryData['totalRecords'] = taskSummaryObj['totalRecords']['values'][0]['value']
                taskSummaryData['totalLoadError'] = taskSummaryObj['totalLoadError']['values'][0]['value']
                taskSummaryData['totalRDPErrors'] = taskSummaryObj['totalRDPErrors']['values'][0]['value']
                taskSummaryData['totalExtractError'] = taskSummaryObj['totalExtractError']['values'][0]['value']
                taskSummaryData['totalRecordsSuccess'] = taskSummaryObj['totalRecordsSuccess']['values'][0]['value']
                taskSummaryData['totalRecordsProcessed'] = taskSummaryObj['totalRecordsProcessed']['values'][0]['value']
                taskSummaryData['totalRecordsCreate'] = taskSummaryObj['totalRecordsCreate']['values'][0]['value']
                taskSummaryData['totalRecordsUpdate'] = taskSummaryObj['totalRecordsUpdate']['values'][0]['value']
                taskSummaryData['totalRecordsDelete'] = taskSummaryObj['totalRecordsDelete']['values'][0]['value']
                taskSummaryData['totalRecordsNoChange'] = taskSummaryObj['totalRecordsNoChange']['values'][0]['value']
                if 'taskAttemptCount' in taskSummaryObj:
                    taskSummaryData['taskAttemptCount'] = taskSummaryObj['taskAttemptCount']['values'][0]['value']

                totalExternalEvents = getTotalExternalEvents(taskSummaryObj['taskId']['values'][0]['value'], str(t))

                if taskSummaryData['taskType'] == 'ENTITY_IMPORT':
                    totalManageEvents = getTotalManageEvents(taskSummaryObj['taskId']['values'][0]['value'], str(t))
                    totalGovernEvents = getTotalGovernEvents(taskSummaryObj['taskId']['values'][0]['value'], str(t))
                    totalRequestObjects = getTotalRequestObjects(taskSummaryObj['taskId']['values'][0]['value'], str(t))

                else:
                    totalManageEvents = 0
                    totalGovernEvents = 0
                    totalRequestObjects = 0

                utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                json_tmp = [{
                    "measurement": measurement,
                    "tags": {
                        "envname": env,
                        "Tenant": str(t),
                        "Profile": taskSummaryData['profileName'],
                        "Type": taskSummaryData['taskType']
                    },
                    "time": utc_time,
                    "fields": {
                        "User": taskSummaryData['userId'],
                        "TaskId": taskSummaryData['taskId'],
                        "Status": taskSummaryData['status'],
                        "Count": taskSummaryData['totalRecords'],
                        "LoadError": taskSummaryData['totalLoadError'],
                        "RDPErrors": taskSummaryData['totalRDPErrors'],
                        "ExtractError": taskSummaryData['totalExtractError'],
                        "Attempt": taskSummaryData['taskAttemptCount'],
                        "Success": taskSummaryData['totalRecordsSuccess'],
                        "Processed": taskSummaryData['totalRecordsProcessed'],
                        "Create": taskSummaryData['totalRecordsCreate'],
                        "Update": taskSummaryData['totalRecordsUpdate'],
                        "Delete": taskSummaryData['totalRecordsDelete'],
                        "NoChange": taskSummaryData['totalRecordsNoChange'],
                        "ExternalEvents": totalExternalEvents,
                        "ManageEvents": totalManageEvents,
                        "GovernEvents": totalGovernEvents,
                        "RequestObjects": totalRequestObjects
                    }
                }
                ]
                json_body.extend(json_tmp)
                time.sleep(3)
        time.sleep(5)
    uc.insert_to_influx(json_body, 'app_metrics')

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
