try:
    import json
    import base64
    import requests
    import sys
    import traceback
except Exception as error:
    print(error)
    sys.exit(201)

try:
    TIMEOUT = 60  #sec
    DOMAIN = 'eastus.azuredatabricks.net'
    TOKEN = b'dapi059eecaf6835aafbd02def39b82f7976'
    BASE_URL = 'https://%s/api/2.0/jobs/list' % (DOMAIN)
    headers = {"Content-Type": "application/json", "Authorization": b"Basic " + base64.standard_b64encode(b"token:" + TOKEN)}

    try:
        response = requests.get(BASE_URL, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            for jobs in response.json()['jobs']:
                job_id = job_name = env_name = tenant_id = last_run = None

                if 'job_id' in jobs:
                    job_id = jobs['job_id']

                try:
                    GET_RUN_URL = 'https://%s/api/2.0/jobs/runs/list?job_id=%s&active_only=false&offset=0&limit=1' % (DOMAIN, job_id)
                    run_response = requests.get(GET_RUN_URL, headers=headers, timeout=TIMEOUT)
                    if run_response.status_code == 200:

                        if 'has_more' in run_response.json():
                            hasMore = run_response.json()['has_more']

                            if hasMore == False:
                                continue;

                            elif hasMore == True and 'runs' in run_response.json():
                                 for run in run_response.json()['runs']:
                                     if 'state' in run and 'life_cycle_state' in run['state']:
                                         job_life = run['state']['life_cycle_state']
                                         if job_life == 'TERMINATED':
                                             last_run = run['state']['result_state']
                                         elif job_life == 'PENDING' or 'RUNNING':
                                             try:
                                                 GET_PREV_RUN_URL = 'https://%s/api/2.0/jobs/runs/list?job_id=%s&active_only=false&offset=1&limit=1' % (
                                                 DOMAIN, job_id)
                                                 run_response_prev = requests.get(GET_PREV_RUN_URL, headers=headers,
                                                                                  timeout=TIMEOUT)
                                                 if run_response_prev.status_code == 200:
                                                     for run_sec in run_response_prev.json()['runs']:
                                                        last_run = run_sec['state']['result_state']
                                             except requests.exceptions.Timeout:
                                                 print('request %s timed out (', TIMEOUT, 'sec) <br>' % (DOMAIN))
                                                 sys.exit(2)
                                             except requests.exceptions.RequestException as e:
                                                 print('Error fetching azure databricks job data:', str(e))
                                                 sys.exit(2)
                            if 'settings' in jobs and 'name' in jobs['settings']:
                                job_name = jobs['settings']['name']

                            if 'settings' in jobs and 'notebook_task' in jobs['settings'] and 'base_parameters' in \
                                    jobs['settings'][
                                        'notebook_task'] and 'cluster' in jobs['settings']['notebook_task'][
                                'base_parameters']:
                                env_name = jobs['settings']['notebook_task']['base_parameters']['cluster']

                            if 'settings' in jobs and 'notebook_task' in jobs['settings'] and 'base_parameters' in \
                                    jobs['settings'][
                                        'notebook_task'] and 'tenantId' in jobs['settings']['notebook_task'][
                                'base_parameters']:
                                tenant_id = jobs['settings']['notebook_task']['base_parameters']['tenantId']


                    else:
                        print("Error!")

                except requests.exceptions.Timeout:
                    print('request %s timed out (', TIMEOUT, 'sec) <br>' % (DOMAIN))
                    sys.exit(2)
                except requests.exceptions.RequestException as e:
                    print('Error fetching azure databricks job data:', str(e))
                    sys.exit(2)

                print("%s %s %s %s %s" % (job_id, env_name, tenant_id, job_name, last_run))


    except requests.exceptions.Timeout:
        print('request %s timed out (', TIMEOUT, 'sec) <br>' % (DOMAIN))
        sys.exit(2)
    except requests.exceptions.RequestException as e:
        print('Error fetching azure databricks job data:', str(e))
        sys.exit(2)


except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
