try:
  import sys
  import traceback
  import loadmodules
  from jira import JIRA
  import re
  from datetime import datetime
  import os
except Exception as error: 
    print(error)
    sys.exit(201)
try:
  def jira(ticketName):
    alert_list = []
    user = 'l1support@riversand.com'
    apikey = 'dnKRnucmliou2wA9dXfj1C5C'
    server = 'https://riversand.atlassian.net'
    options = {
        'server': server
    }
    jira = JIRA(options, basic_auth=(user, apikey))
    summary = '"' + 'ENV:' + os.environ['envname'] + '"'
    issues = jira.search_issues(
        'project=OPS' and 'summary~'+summary, maxResults=500)
    issue_details = [[issue.fields.summary] +
                     [issue.fields.created] + [issue.fields.status] for issue in issues]
    for tickets in issue_details:
      ticket_name = tickets[0]
      created_date = str(tickets[1])
      status = tickets[2]
      status = str(status)
      created_date_split = created_date.split('T')
      time_hrs_mints_secs = created_date_split[1].split('.')[0]
      date_time_obj = datetime.strptime(
          (created_date_split[0]+" " + time_hrs_mints_secs).strip(), '%Y-%m-%d %H:%M:%S')
      ticket_age_in_days = ((datetime.now() - date_time_obj).days)
      if 'ALERT' in ticket_name and ticket_age_in_days <= 2:
        if status == 'Work in progress' or status == 'Waiting for support' or status == 'Open':
          alert_list.append(ticket_name)
    for alert in alert_list:
      if alert == ticketName:
        return True
        break
except Exception as error:
    print(error)
    traceback.print_exc()
    sys.exit(201)
