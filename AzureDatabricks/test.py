import croniter
import datetime

now = datetime.datetime.now()
sched = '1 15 1,15 * *'    # at 3:01pm on the 1st and 15th of every month
cron = croniter.croniter(sched, now)

for i in range(4):
    nextdate = cron.get_next(datetime.datetime)
    print (nextdate)