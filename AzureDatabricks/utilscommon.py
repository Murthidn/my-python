# collection of resusable functions
try:
    import sys
    import traceback
    import loadmodules
    import time
    from influxdb import InfluxDBClient
    from influxdb.exceptions import InfluxDBClientError
    from influxdb.exceptions import InfluxDBServerError
    from datetime import datetime
    from datetime import timedelta
    import os
    import json
    import requests
    from requests.packages.urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter
except Exception as error:
    print(error)
    sys.exit(201)
try:
    def log_influx_errors(type, data, msg):
        try:
            with open('/rootfs/etc/hostname', 'r') as hostnameinfo:
                hostname = hostnameinfo.read().strip()
        except:
            print('Exception error while opening /rootfs/etc/hostname')
            sys.exit(201)
        with open('/rootfs/home/ubuntu/sensu/logs/influx_errors.log', 'a') as f:
            time_ist = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
            f.write(
                '-----' + '\n' + '[' + time_ist + ' IST] from host: ' + hostname + '\n' + type + ': ' + data + ', ' + msg + '\n')


    def insert_to_influx(jsondata, database):
        """
        insert some data into an influx measurement
        """
        client = InfluxDBClient(host='influxdb', port=8186, database=database)
        count = 0
        while True:
            try:
                client.write_points(jsondata)
                client.close()
                break
            except Exception as e:
                client.close()
                log_influx_errors('ERROR', str(jsondata), str(e))
                count = count + 1
                if count == 4:
                    print("could not insert data into influx")
                    sys.exit(2)
                else:
                    time.sleep(5)
        return True


    def query_influx(query, database):
        """
        get data from influx
        """
        client = InfluxDBClient(host='influxdb', port=8186, database=database)
        count = 0
        while True:
            try:
                rs = client.query(query)
                client.close()
                break
            except Exception as e:
                client.close()
                log_influx_errors('ERROR', query, str(e))
                count = count + 1
                if count == 4:
                    sys.exit(2)
                else:
                    time.sleep(5)
        return rs


    def ping_influx():
        """
        ping influx to see if its running and reachable
        """
        TIMEOUT = 3  # sec
        url = 'http://influxdb:8186/ping'
        try:
            r = requests.get(url, timeout=TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.Timeout as e:
            log_influx_errors('ERROR', 'influx not reachable - request timed out' + str(TIMEOUT) + ' sec', str(e))
            return False
        except requests.exceptions.RequestException as e:
            log_influx_errors('ERROR', 'influx not reachable - exception encountered:', str(e))
            return False
        else:
            if r.status_code == 204:
                return True
            else:
                log_influx_errors('ERROR', 'influx not reachable. Http code:', str(r.status_code))
                return False


    def check_http_get(url, timeout=10):
        """
        check if http get on url returns 200 (ok) response
        """
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
        except requests.exceptions.Timeout as e:
            return False
        except requests.exceptions.RequestException as e:
            return False
        else:
            if r.status_code != 200:
                return False
            else:
                return True


    def rdp_ver_lt(threshold):
        """
        goal: check if rdp version is less than 'threshold'
        rdp version refers to second octet for e.g. '44' in  '1.44.0.23'
        logic:
            get rdp version from sensu stash
            if no data:
                get data from rdp-rest:8085

        Note: hdfs and hbase has been removed since rdp v47
        any exception in getting data in this function results in returning 'False'
        which implies ver is 47 or above, hence dont process checks
        related to hdfs and hbase
        """
        s = requests.Session()
        retries = Retry(total=1,
                        backoff_factor=0.2,
                        status_forcelist=[400, 403, 404, 408, 409, 500, 502, 503, 504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        try:
            res = s.get('http://sensu-server:4567/stashes/rdp_version', timeout=1)
            res.raise_for_status()
        except Exception as e:
            # get data from rdp-rest:8085
            try:
                rdp_url = 'http://rdp-rest:8085'
                r = s.get(rdp_url, timeout=1)
                r.raise_for_status()
            except Exception as e:
                # print 'Exception raised when getting rdp version from rdp-rest'
                exit_code = 1
            else:
                if r.status_code == 200:
                    # ok got data from rdp-rest
                    rdp_version = int(r.json()['version'].split('.')[1])
                    if rdp_version < threshold:
                        # print 'rdp-rest: rdp version ' + str(rdp_version) + ' is less than 47'
                        return True
                    else:
                        # print 'rdp:rest: rdp version ' + str(rdp_version) + ' is >= than 47'
                        return False
                else:
                    return False
        else:
            if res.status_code == 200:
                # process
                rdp_version = int(res.json()['rdp_version'])
                if rdp_version < threshold:
                    # print 'sensu stash: rdp version ' + str(rdp_version) + ' is less than 47'
                    return True
                else:
                    # print 'sensu stash: rdp version ' + str(rdp_version) + ' is >= 47'
                    return False
            else:
                # error
                # print 'incorrect status code from sensu stash ' + str(res.status_code)
                return False


    def keys_exists(element, *keys):
        """
        helper function to check if a nested key exists in a dictionary
        """
        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return True
except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
