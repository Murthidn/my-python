import json
import os

cmd = "curl -G 'http://influxdb:8186/query?pretty=true' --data-urlencode 'db=sensu' --data-urlencode 'q=SELECT * FROM CPU_Usage order by desc limit 100'"
result = os.system(cmd)

s=str(result)

d = json.load(s)

print(type(d))