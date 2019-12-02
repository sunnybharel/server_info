import pycurl
from io import BytesIO
import json
import re
import pandas as pd

MEM_ALARM = 90
CPU_ALARM = 90


def poll_for_server_list(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    temp_list = []
    for item in json.loads(buffer.getvalue()):
        temp_list.append(item)
    return temp_list


def poll_for_detailed_server_info(list, server_ip):
    json_object = []
    for server_to_poll in list:
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, server_ip + server_to_poll)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        json_object.append(json.loads(buffer.getvalue()))
    return json_object


def decide_status(row):
    if int(row['cpu']) > 89 or int(row['memory']) > 89:
        return 'Unhealthy'
    else:
        return 'Healthy'

if __name__ == '__main__':
    server_ip = 'http://localhost:8080/'
    url = server_ip + 'servers'
    server_list = poll_for_server_list(url)
    df = pd.read_json(json.dumps(poll_for_detailed_server_info(server_list, server_ip)))
    df['server'] = server_list
    df['cpu'] = df['cpu'].apply(lambda x: re.sub('%', '', str(x)))
    df['memory'] = df['memory'].apply(lambda x: re.sub('%', '', str(x)))
    df['cpu'] = pd.to_numeric(df['cpu'])
    df['memory'] = pd.to_numeric(df['memory'])
    df['status'] = ""
    df['status'] = df.apply(lambda x: decide_status(x), axis=1)
    print("OPTION 1")
    print(df)  # Printed Option 1

    print("OPTION 2")
    print(df.groupby(['service']).mean())  # Printed Option 2
    after = df[df['status'] == 'Healthy']
    after = df.groupby(['service']).size()
    print("OPTION 3")
    print(after[after < 2])  # Printed Option 3
