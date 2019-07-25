try:
    import sys
    import os
    import json
    import base64
    import traceback

    sys.path.insert(0, '/usr/python-packages/dn-requests/')
    import requests

    from datetime import datetime
    sys.path.insert(0, '/usr/python-packages/dn-influxdb/')

    from influxdb import InfluxDBClient
    from influxdb.exceptions import InfluxDBClientError

    from helper import *
    #from AzureDatabricks.helper import *

except Exception as error:
    print(error)
    sys.exit(201)

try:
    ENV_NAME = os.environ['envname']
    LOCATION=getAzureRegionName()
    DOMAIN = LOCATION + '.azuredatabricks.net'
    SUBSCRIPTION = os.environ['subscription'] #'Riversand Violet - Non-Production'
    getNetrcFile(LOCATION, SUBSCRIPTION)
    TOKEN = getDatabricksTokenFromNetrcFile()
    HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN}
    client = InfluxDBClient(host='influxdb', port=8186, database='sensu')

    def getJobData(env_name, job_id):
        RUNS_URL = 'https://%s/api/2.0/jobs/runs/list?job_id=%s&active_only=false&offset=0&limit=1' % (DOMAIN, job_id)
        job_runs = clientRequest(RUNS_URL, HEADERS)

        if job_runs.status_code == 200 and 'has_more' in job_runs.json():
            isHasMore = job_runs.json()['has_more']

            if isHasMore == True or 'runs' in job_runs.json():
                for run in job_runs.json()['runs']:

                    if 'state' in run and 'life_cycle_state' in run['state']:
                        job_life = run['state']['life_cycle_state']

                        if job_life == 'TERMINATED':
                            last_run = run['state']['result_state']

                        if job_life == 'INTERNAL_ERROR':
                            last_run = run['state']['result_state']

                        elif job_life == 'SKIPPED':
                            last_run = 'SKIPPED'

                        # If current Job is in Pending or Running state, getting previous job status
                        elif job_life == 'PENDING' or job_life == 'RUNNING':
                            PREV_RUNS_URL = 'https://%s/api/2.0/jobs/runs/list?job_id=%s&active_only=false&offset=1&limit=1' % (DOMAIN, job_id)
                            job_run_prev = clientRequest(PREV_RUNS_URL, HEADERS)

                            if job_run_prev.status_code == 200:
                                for second_run in job_run_prev.json()['runs']:

                                    if 'state' in second_run and 'life_cycle_state' in second_run['state']:
                                        job_life = second_run['state']['life_cycle_state']

                                        if job_life == 'TERMINATED':
                                            last_run = second_run['state']['result_state']

                                        elif job_life == 'INTERNAL_ERROR':
                                            last_run = run['state']['result_state']

                                        elif job_life == 'SKIPPED':
                                            last_run = 'SKIPPED'

                        if last_run == 'CANCELED' or last_run == 'FAILED' or last_run == 'SKIPPED':
                            last_run_status = 1

                        elif last_run == 'SUCCESS':
                            last_run_status = 0

                if 'settings' in job and 'name' in job['settings']:
                    job_name = job['settings']['name']

                if 'settings' in job and 'notebook_task' in job['settings'] and 'base_parameters' in job['settings']['notebook_task'] and 'tenantId' in job['settings']['notebook_task']['base_parameters']:
                    tenant_id = job['settings']['notebook_task']['base_parameters']['tenantId']

                else:
                    if 'settings' in job and 'new_cluster' in job['settings'] and 'custom_tags' in job['settings']['new_cluster'] and 'TENANT_ID' in job['settings']['new_cluster']['custom_tags']:
                        tenant_id = job['settings']['new_cluster']['custom_tags']['TENANT_ID']

                print(job_id, env_name, tenant_id, job_name, last_run, last_run_status)

                # Writing results into Influx (5)
                measurement = 'pd_jobs_status'
                utc_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                json_body = [{
                    "measurement": measurement,
                    "tags": {
                        "jobid": job_id,
                        "envname": env_name,
                        "tenant": tenant_id,
                        "jobname": job_name,
                        "lastrun": last_run
                    },
                    "time": utc_time,
                    "fields": {
                        "status": last_run_status
                    }
                }]
                try:
                    client.write_points(json_body)
                except InfluxDBClientError as e:
                    print('ERROR: could not insert data to influxdb:', str(e))
                except:
                    e = sys.exc_info()[0]
                    print('ERROR: could not insert data to influxdb:', str(e))
                else:
                    pass

    LIST_URL = 'https://%s/api/2.0/jobs/list' % (DOMAIN)
    jobs = clientRequest(LIST_URL, HEADERS)

    if jobs.status_code == 200:
        for job in jobs.json()['jobs']:

            if 'settings' in job and 'notebook_task' in job['settings'] and 'base_parameters' in job['settings'][
                'notebook_task'] and 'cluster' in job['settings']['notebook_task']['base_parameters']:
                env_name = job['settings']['notebook_task']['base_parameters']['cluster']
                if env_name == ENV_NAME:
                    getJobData(env_name, job['job_id'])

            elif 'settings' in job and 'new_cluster' in job['settings'] and 'custom_tags' in job['settings'][
                'new_cluster'] and 'ENV_NAME' in job['settings']['new_cluster']['custom_tags']:
                env_name = job['settings']['new_cluster']['custom_tags']['ENV_NAME']
                if env_name == ENV_NAME:
                    getJobData(env_name, job['job_id'])

    client.close()
    sys.exit(201)

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
