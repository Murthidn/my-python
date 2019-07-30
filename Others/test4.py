try:
    import sys
    import traceback
    import os
    import sys
    import utilscommon as uc
    import os
    import utilscommon as uc
    import argparse
    import loadmodules
    import requests
    import influxdbjira
    import jiracheck as ji
except Exception as error:
    print(error)
    sys.exit(201)
try:
    env = os.environ['envname']
    parser = argparse.ArgumentParser()
    parser.add_argument("metrictype", help="metric type: disk / cpu / memory")
    parser.add_argument("measurement", help="influx measurement (table) name")
    parser.add_argument("-c", "--critical", type=int,
                        help="critical threshold - int 1 to 100")
    parser.add_argument("-w", "--warning", type=int,
                        help="warning threshold - int 1 to 100")
    parser.add_argument("-d", "--duration",
                        help="duration calculating mean e.g. 15m, 2h")
    parser.add_argument("--check", type=str)
    args = parser.parse_args()
    check = args.check
    with open('/rootfs/etc/hostname', 'r') as hostnameinfo:
        hostname = hostnameinfo.read().strip()
    try:
        if len(check) != 0:
            possible_alert_name = "ENV:" + env + "|ALERT:" + hostname + "/" + check + ":CRITICAL"
    except:
        pass


    def check_thresholds(val):
        if args.metrictype == 'disk':
            if args.critical is not None:
                if val >= args.critical:
                    if ji.jira(possible_alert_name):
                        print("jiraticketexists")
                    else:
                        print(args.metrictype + ' usage (' + str(val) +
                              '%) has reached or crossed critical threshold of ' + str(args.critical) + '%')
                    sys.exit(2)

            if args.warning is not None:
                if val >= args.warning:
                    print(args.metrictype + ' usage (' + str(val) +
                          '%) has reached or crossed warning threshold of ' + str(args.warning) + '%')
                    sys.exit(0)
            print(args.metrictype + ' usage (' + str(val) +
                  '%) is within the threshold limits.')
        else:  # cpu or memory
            if args.critical is not None:
                if args.metrictype == 'memory':
                    if val >= args.critical:
                        if len(check) != 0:
                            if ji.jira(possible_alert_name):
                                print("jiraticketexists")
                            else:
                                print('Average ' + args.metrictype + ' usage (' + str(val) + '%) across last ' +
                                      args.duration + ' reached or crossed critical threshold of ' + str(
                                    args.critical) + '%')
                            sys.exit(2)
                        else:
                            print('Average ' + args.metrictype + ' usage (' + str(val) + '%) across last ' +
                                  args.duration + ' reached or crossed critical threshold of ' + str(
                                args.critical) + '%')
                            sys.exit(2)
                else:
                    if val >= args.critical:
                        print('Average ' + args.metrictype + ' usage (' + str(val) + '%) across last ' +
                              args.duration + ' reached or crossed critical threshold of ' + str(args.critical) + '%')
                        sys.exit(2)

            if args.warning is not None:
                if val >= args.warning:
                    print('Average ' + args.metrictype + ' usage (' + str(val) + '%) across last ' +
                          args.duration + ' reached or crossed warning threshold of ' + str(args.warning) + '%')
                    sys.exit(0)
            print(args.metrictype + ' usage (' + str(val) +
                  '%) is within the threshold limits.')


    # execution starts here -->
    # skip execution if rdp ver >= 47 and disk type is hdfs
    if uc.rdp_ver_lt(47) == False:
        if args.measurement in ['disk_data_hdfs', 'disk_data_hdfs_namenode1', 'disk_data_hdfs_namenode2']:
            print('Skipping alert as rdp ver >= 47 and disk type is hdfs')
            sys.exit(0)

    # form the query based on type of metric
    if args.metrictype == 'disk':
        qry = 'select value from {m} where host = \'{h}\' order by time desc LIMIT 1'.format(
            m=args.measurement, h=hostname)
    elif args.metrictype == 'cpu':
        qry = 'select MEAN(value) from {m} WHERE time > now() - {t} and host = \'{h}\' '.format(
            m=args.measurement, t=args.duration, h=hostname)
    elif args.metrictype == 'memory':
        qry = 'select MEAN(value) from {m} WHERE time > now() - {t} and host = \'{h}\' '.format(
            m=args.measurement, t=args.duration, h=hostname)
    else:
        print('no metric type provided')
        sys.exit(0)

    # run query and check if threshold is crossed
    if uc.ping_influx():
        rs = uc.query_influx(qry)
        if rs is not None and len(rs) > 0:
            if args.metrictype == 'disk':
                val = next(list(rs.items())[0][1])['value']
                check_thresholds(val)
            elif args.metrictype == 'cpu' or args.metrictype == 'memory':
                val = next(list(rs.items())[0][1])['mean']
                check_thresholds(val)
            else:
                val = 0
        else:
            print('Error: influx query did not return any data.')
            sys.exit(201)
    else:
        print('Error: could not reach influx.')
        sys.exit(201)
except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
