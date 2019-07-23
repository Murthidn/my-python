import base64

#tk='UNdapi059eecaf6835aafbd02def39b82f7976'
TOKEN = 'dapi059eecaf6835aafbd02def39b82f7976'

#TOKEN='b'+ '\'' + TOKEN1+ '\''


HEADERS = {"Content-Type": "application/json", "Authorization": b"Basic " + base64.standard_b64encode(b"token:" + b'TOKEN')}

print(TOKEN)
