try:
    import sys
    import traceback
    import json
    import os
    import loadmodules
    import utilscommon as uc
    import re
    from datetime import datetime
    import requests
    import jiracheck as ji
    import time

except Exception as error:
    print(error)
    sys.exit(201)

try:
    env = os.environ['envname']
    measurement_name = 'autoHealing_upon_error'
    TIMEOUT = 60  # sec
    bolt_error = '[ { \'time\': \'2019-09-26T04:15:20Z\', \'topology_name\': \'configurationManageService\', \'bolt_id\': \'configmanage-searchcreate-bolt\', \'last_error\': \'java.lang.NoClassDefFoundError: Could not initialize class com.riversand.dataplatform.es.searchmanager.data.esclient.SearchManagerDA\\n\tat com.riversand.dataplatform.ts.searchmanager.SearchManagerBL.<in\' } ]'
    spout_error = ''
    bolt_services = {}
    spout_services = {}
    bolt_services_oom = {}
    spout_services_oom = {}

    check = sys.argv[1]
    possible_alert_name = "ENV:" + env + "|ALERT:proxyclient/" + check + ":CRITICAL"


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


    def alert(services):
        counter = 0
        showheader = True
        if ji.jira(possible_alert_name):
            print("jiraticketexists")
            sys.exit(2)
        else:
            for error, service in services.items():
                for i in service:
                    counter += 1
                    state = 'CRITICAL'
                    if showheader == True:
                        print('<h4> Auto healing threshold reached!! </h4>')
                        print('<table class="tg">')
                        print('<tr>')
                        print('<th>#</th>')
                        print('<th>Service Name</th>')
                        print('<th>Error</th>')
                        print('</tr>')
                        showheader = False
                    print('<tr>')
                    print('<td>' + str(counter) + '</td>')
                    print('<td>' + str(i) + '</td>')
                    print('<td>' + str(error) + '</td>')
                    print('</tr>')

        if state == 'CRITICAL':
            print('</table>')
            sys.exit(2)


    def autoheal(error_service):
        url = ('http://rdp-rest:8085/dataplatform/api/adminservice/deploytopology')
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-rdp-userId': 'system_user',
                   'x-rdp-userRoles': '["admin"]'}
        utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        json_body = []
        for error, service in error_service.items():
            for i in service:
                if 'rsConnectService' in i:
                    if i == 'rsConnectService-import':
                        inboundDomain = 'import'
                    else:
                        inboundDomain = 'export'
                    query = {'adminObject': {'id': 'someguid', 'type': 'adminObject',
                                             'properties': {'serviceName': 'rsConnectService',
                                                            'inboundDomain': str(inboundDomain), 'action': 'restart',
                                                            'waitBeforeStartInSec': 5}}}
                else:
                    query = {'adminObject': {'id': 'someguid', 'type': 'adminObject',
                                             'properties': {'serviceName': str(i), 'action': 'restart',
                                                            'waitBeforeStartInSec': 5}}}
                time.sleep(2)
                response = requesthelper(url, query, headers, TIMEOUT)
                print(response)
                json_tmp = [{
                    "measurement": measurement_name,
                    "tags": {
                        "envname": env,
                        "servicename": i,
                    },
                    "time": utc_time,
                    "fields": {
                        "error": error
                    }
                }]
                json_body.extend(json_tmp)
        uc.insert_to_influx(json_body, 'tech_metrics')


    def validate_no_of_healing(rs, error_service):
        error_counter = {}
        threshold = 2
        services = []
        service_to_heal = {}
        service_to_alert = {}

        for error, svc in error_service.items():
            for i in svc:
                if i not in services:
                    services.append(i)
        for service in services:
            # Rating every service per error
            data = list(rs.get_points(tags={'servicename': service}))
            for i in data:
                key = i['error'] + "_" + service
                if key in error_counter:
                    error_counter[key] = error_counter[key] + 1
                else:
                    error_counter[key] = 1
        # Storing the service with error message, which comes for the very first time
        for error, service in error_service.items():
            for i in service:
                key = error + "_" + i
                if key not in error_counter:
                    error_counter[key] = 1

        # Deriving the services for healing and alerting
        for error, count in error_counter.items():
            if count == 1:
                err = error.split("_")[0]
                service = error.split("_")[1]
                if err not in service_to_heal:
                    service_to_heal[err] = [service]
                else:
                    service_to_heal[err].append(service)
            else:
                err = error.split("_")[0]
                service = error.split("_")[1]
                if err not in service_to_alert:
                    service_to_alert[err] = [service]
                else:
                    service_to_alert[err].append(service)
        if service_to_heal:
            autoheal(service_to_heal)
        if service_to_alert:
            alert(service_to_alert)


    query = ('select error from ' + str(
        measurement_name) + ' where time > now() - 24h group by servicename order by time desc')
    rs = uc.query_influx(query, 'tech_metrics')

    print(rs)
    if rs is None or len(rs) <= 0:
        if bolt_error:
            for i in bolt_error:
                servicename = i['topology_name']
                if 'OutOfMemoryError' not in i['last_error']:
                    if i['last_error'] in bolt_services:
                        if servicename not in bolt_services[i['last_error']]:
                            bolt_services[i['last_error']].append(servicename)
                    else:
                        bolt_services[i['last_error']] = [servicename]
                else:
                    if i['topology_name'] not in bolt_services_oom:
                        bolt_services_oom[i['last_error']] = servicename
        if spout_error:
            for i in spout_error:
                servicename = i['topology_name']
                if 'OutOfMemoryError' not in i['last_error']:
                    if i['last_error'] in spout_services:
                        if servicename not in spout_services[i['last_error']]:
                            spout_services[i['last_error']].append(servicename)
                    else:
                        spout_services[i['last_error']] = [servicename]
                else:
                    if i['topology_name'] not in spout_services_oom:
                        spout_services_oom[i['last_error']] = servicename
        if bolt_services:
            autoheal(bolt_services)
        if spout_services:
            autoheal(spout_services)
        if bolt_services_oom:
            alert(bolt_services_oom)
        if spout_services_oom:
            alert(spout_services_oom)
    elif bolt_error:
        for i in bolt_error:
            servicename = i['topology_name']
            if 'OutOfMemoryError' not in i['last_error']:
                if i['last_error'] in bolt_services:
                    if servicename not in bolt_services[i['last_error']]:
                        bolt_services[i['last_error']].append(servicename)
                else:
                    bolt_services[i['last_error']] = [servicename]
        validate_no_of_healing(rs, bolt_services)
    elif spout_error:
        for i in spout_error:
            servicename = i['topology_name']
            if 'OutOfMemoryError' not in i['last_error']:
                if i['last_error'] in spout_services:
                    # Creating collection of values to handle multiple service with same error
                    if servicename not in spout_services[i['last_error']]:
                        spout_services[i['last_error']].append(servicename)
                else:
                    spout_services[i['last_error']] = [servicename]
        validate_no_of_healing(rs, spout_services)
except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)