try:
    import sys
    import traceback
    import os
    import utilscommon as uc
except Exception as error:
    print(error)
    sys.exit(201)
try:
    counter = 0
    critical = False
    exit_status = 0
    check = sys.argv[1]
    env_name = os.environ['envname']
    query = ("select * from pd_jobs_status where lastrun = 'FAILED' and time >= now() - 30m order by time desc")
    rs = uc.query_influx(query)
    if rs is None or len(rs) <= 0:
        print("No Jobs are failed in last 30 minutes")
        sys.exit(0)
    elif len(rs) > 0:
        critical = True
    if critical:
        print('<h4>PD Job Status</h4>')
        for k, v in rs.items():
            print('<table class="tg">')
            print('<tr>')
            print('<th>#</th>')
            print('<th>jobid</th>')
            print('<th>envname</th>')
            print('<th>tenant</th>')
            print('<th>jobname</th>')
            print('<th>lastrun</th>')
            print('<th>status</th>')
            print('</tr>')
            for val in v:
                counter += 1
                print('<tr>')
                print('<td>' + str(counter) + '</td>')
                print('<td>' + str(val['jobid']) + '</td>')
                print('<td>' + str(val['envname']) + '</td>')
                print('<td>' + str(val['tenant']) + '</td>')
                print('<td>' + str(val['jobname']) + '</td>')
                print('<td>' + str(val['lastrun']) + '</td>')
                print('<td>' + str(val['status']) + '</td>')
                print('</tr>')
        exit_status = 2

    sys.exit(exit_status)
except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
