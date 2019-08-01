import sys

rsdata=1
if rsdata == 0:
    print("Error: No datapoints found in InfluxDB")
    sys.exit(2)

elif rsdata > 0:
    print("has data")