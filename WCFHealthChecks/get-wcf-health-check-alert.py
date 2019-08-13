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
    query = ("SELECT * FROM wcf_healthcheck_data WHERE status=1 and time >= now() - 5m order by time desc")
    rs = uc.query_influx(query)
    if rs is None:
        print("WARNING: Could not fetch data from influxdb")
        sys.exit(201)
    else:
        rsdata = list(rs.get_points())
    if len(rsdata) == 0:
        print("WCF Communication from RDP is fine in last 5 minutes")
        sys.exit(2)
    elif len(rsdata) > 0:
        critical = True
    if critical:
        print('<h4>WCF Communication Failed Status</h4>')
        for k, v in rs.items():
            print('<table class="tg">')
            print('<tr>')
            print('<th>#</th>')
            print('<th>tenant</th>')
            print('</tr>')
            for val in v:
                counter += 1
                print('<tr>')
                print('<td>' + str(counter) + '</td>')
                print('<td>' + str(val['tenant']) + '</td>')
                print('</tr>')
        exit_status = 2
    sys.exit(exit_status)
except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)