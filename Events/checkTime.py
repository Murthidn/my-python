import datetime
from datetime import timedelta

datetimeFormat = '%Y-%m-%dT%H:%M.f'
date1 = '2019-09-28T07:35:45.223-0500'
date2 = '2019-09-28T07:35:45.223-0500'
diff = datetime.datetime.strptime(date1, datetimeFormat) \
       - datetime.datetime.strptime(date2, datetimeFormat)

print("Difference:", diff)
print("Days:", diff.days)
print("Microseconds:", diff.microseconds)
print("Seconds:", diff.seconds)