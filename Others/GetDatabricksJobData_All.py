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
    TOKEN = 'dapi059eecaf6835aafbd02def39b82f7976'
    LIST_URL = 'https://%s/api/2.0/jobs/list' % (DOMAIN)
    HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN}

    try:
        jobs = requests.get(LIST_URL, headers=HEADERS, timeout=TIMEOUT)
        if jobs.status_code == 200:

            for job in jobs.json()['jobs']:
                job_id = job_name = env_name = tenant_id = last_run = None

                if 'job_id' in job:
                    job_id = job['job_id']

                try:
                    RUNS_URL = 'https://%s/api/2.0/jobs/runs/list?job_id=%s&active_only=false&offset=0&limit=1' % (DOMAIN, job_id)
                    job_runs = requests.get(RUNS_URL, headers=HEADERS, timeout=TIMEOUT)

                    if job_runs.status_code == 200:
                        if 'has_more' in job_runs.json():
                            isHasMore = job_runs.json()['has_more']

                            if isHasMore == False:
                                continue;

                            elif isHasMore == True and 'runs' in job_runs.json():
                                 for run in job_runs.json()['runs']:

                                     if 'state' in run and 'life_cycle_state' in run['state']:
                                         job_life = run['state']['life_cycle_state']

                                         if job_life == 'TERMINATED':
                                             last_run = run['state']['result_state']

                                         elif job_life == 'PENDING' or 'RUNNING':
                                             try:
                                                 PREV_RUNS_URL = 'https://%s/api/2.0/jobs/runs/list?job_id=%s&active_only=false&offset=1&limit=1' % (DOMAIN, job_id)
                                                 job_run_prev = requests.get(PREV_RUNS_URL, headers=HEADERS, timeout=TIMEOUT)

                                                 if job_run_prev.status_code == 200:
                                                     for second_run in job_run_prev.json()['runs']:

                                                        last_run = second_run['state']['result_state']

                                             except requests.exceptions.Timeout:
                                                 print('request %s timed out (', TIMEOUT, 'sec) <br>' % (DOMAIN))
                                                 sys.exit(2)

                                             except requests.exceptions.RequestException as e:
                                                 print('Error fetching azure databricks job data:', str(e))
                                                 sys.exit(2)


                                 if 'settings' in job and 'name' in job['settings']:
                                     job_name = job['settings']['name']

                                 if 'settings' in job and 'notebook_task' in job['settings'] and 'base_parameters' in job['settings']['notebook_task'] and 'cluster' in job['settings']['notebook_task']['base_parameters']:
                                     env_name = job['settings']['notebook_task']['base_parameters']['cluster']

                                 else:
                                     if 'settings' in job and 'new_cluster' in job['settings'] and 'custom_tags' in job['settings']['new_cluster'] and 'ENV_NAME' in job['settings']['new_cluster']['custom_tags']:
                                        env_name = job['settings']['new_cluster']['custom_tags']['ENV_NAME']

                                 if 'settings' in job and 'notebook_task' in job['settings'] and 'base_parameters' in job['settings']['notebook_task'] and 'tenantId' in job['settings']['notebook_task']['base_parameters']:
                                     tenant_id = job['settings']['notebook_task']['base_parameters']['tenantId']

                                 else:
                                     if 'settings' in job and 'new_cluster' in job['settings'] and 'custom_tags' in job['settings']['new_cluster'] and 'TENANT_ID' in job['settings']['new_cluster']['custom_tags']:
                                         tenant_id = job['settings']['new_cluster']['custom_tags']['TENANT_ID']

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
