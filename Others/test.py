try:
    import sys
    import traceback
    import os
    import utilscommon as uc
except Exception as error:
    print(error)
    sys.exit(201)
try:
    query = ('SELECT * FROM CPU_Usage order by desc limit 100')
    rs = uc.query_influx(query)
    print(rs)

except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
