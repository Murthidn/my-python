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
    import kafkalagalert as kl
    import jiracheck as ji

except Exception as error:
    print(error)
    sys.exit(201)

try:

    env = os.environ['envname']
    measurement_name = 'autoHealing'
    TIMEOUT = 60 # sec
    topicLagList = kl.final_lag
    #possible_alert_name = "ENV:" + env + "|ALERT:proxyclient/" + check + ":CRITICAL"

    def requesthelper(url, query ,headers,timeout):
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

    def heal(qualified_services):
        url = ('http://rdp-rest:8085/dataplatform/api/adminservice/deploytopology')
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-rdp-userId': 'system_user', 'x-rdp-userRoles': '["admin"]'}
        utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        json_body = []
        services = []
        for service,offset in qualified_services.items():
            if service not in services:
                services.append(service)
                query = {'adminObject': {'id': 'someguid','type': 'adminObject','properties': {'serviceName': str(service),'restart': 'true','waitBeforeStartInSec': 5}}}
                print(query)
                response = requesthelper(url, query, headers, TIMEOUT)
                print(response)
                json_tmp = [{
                        "measurement": measurement_name,
                        "tags": {
                            "envname": env,
                            "servicename": service,
                        },
                        "time": utc_time,
                        "fields": {
                            "count": offset
                        }
                    }]
                json_body.extend(json_tmp)
        uc.insert_to_influx(json_body)
        print(json_body)

    def generate_alert(services):
        counter = 0
        showheader = True
        possible_alert_name = False
        if ji.jira(possible_alert_name):
            print("jiraticketexists")
            sys.exit(2)
        else:
            for service in services:
                counter += 1
                state = 'CRITICAL'
                if showheader == True:
                    print('Below services are identified with unchanged consumer count <br>')
                    print('<table class="tg">')
                    print('<tr>')
                    print('<th>#</th>')
                    print('<th>Service Name</th>')
                    print('</tr>')
                    showheader = False
                print('<tr>')
                print('<td>' + str(counter) + '</td>')
                print('<td>' + str(service) + '</td>')
                print('</tr>')

        if state == 'CRITICAL':
            print('</table>')
            sys.exit(2)

    def validate_consumer_count(rs,list_for_healing):
        print("Validating Consumer Count")
        qualified_set_1 = {}
        alert_list = []
        for service,offset in list_for_healing.items():
            data = list(rs.get_points(tags={'servicename': service}))
            temp_data = {}
            for i in data:
                if service in i['servicename']:
                    print("service %s offset %s count %s" %(service,offset,i['count']))
                    if offset == i['count']:
                        alert_list.append(service)
                    else:
                        temp_data[service] = offset
                        qualified_set_1.update(temp_data)

        if qualified_set_1:
            validate_no_of_healing(rs,qualified_set_1)

        if alert_list:
            generate_alert(alert_list)

    def validate_no_of_healing(rs,qualified_set_1):
        print("validating numb of restarts")
        qualified_set_2 = {}
        alert_list = []
        # Qualifying the services whose occurrence in last 24hrs is <= 2
        for service,offset in qualified_set_1.items():
            ts = [] #timestamp
            data = list(rs.get_points(tags={'servicename': service}))
            temp_data = {}
            for t in data:
                if t['time'] not in ts:
                    ts.append(t['time'])
            if len(ts) < 2:
                for i in data:
                    temp_data[service] = offset
                    qualified_set_2.update(temp_data)
            else:
                alert_list.append(service)

        if qualified_set_2 :
            heal(qualified_set_2)

        if alert_list:
            generate_alert(alert_list)

    if topicLagList is None or len(topicLagList) <= 0:
        print("WARNING: Could not fetch lag details")
        sys.exit(201)

    list_for_healing = {}
    for i in topicLagList:
        service_name = i['service']
        list_for_healing[service_name]  = i['curr_cons_total_count']

    query = ('select servicename,count from ' + str(measurement_name) + ' where time > now() - 24h order by time desc')
    rs = uc.query_influx(query)

    if rs is None or len(rs) <= 0:
        heal(list_for_healing)
    else:
        validate_consumer_count(rs,list_for_healing)

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)