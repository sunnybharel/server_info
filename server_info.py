from mongoengine import *
import datetime
import pycurl
from io import BytesIO
import json
import re
from columnar import columnar
from click import style

MEM_ALARM = 90
CPU_ALARM = 90

# Create mongoDB connection or fail
try:
    connect('server_db', host='localhost', port=27017)

except Exception as e:
    print("DB connection failed ", e)


# Create schema for MongoDB
class Server(Document):
    ip = StringField(required=True)
    cpu = IntField(required=True)
    memory = IntField(required=True)
    service = StringField(required=True, max_length=20)
    status = StringField()
    polled = DateTimeField(default=datetime.datetime.now)


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
    for server_to_poll in list:
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, server_ip + server_to_poll)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        json_object = json.loads(buffer.getvalue())
        server = Server()
        server.ip = server_to_poll
        server.cpu = re.sub("%", "", json_object['cpu'])
        server.memory = re.sub("%", "", json_object['memory'])
        server.service = json_object['service']
        server.save()


def low_healthy_service_check():
    for rec in Server.objects():
        if rec.memory >= MEM_ALARM or rec.cpu >= CPU_ALARM:
            rec.update(status="Unhealthy")
        else:
            rec.update(status="Healthy")


def pretty_print():
    patterns = [
        ('Unhealthy', lambda text: style(text, fg='white', bg='red')),
        ('[9]{1}\d{1}$', lambda text: style(text, fg='white', bg='red')),
    ]
    data = []
    for rec in Server.objects():
        data.append([rec.ip, rec.service, rec.status, rec.cpu, rec.memory])
    table = columnar(data, headers=['IP', 'Service', 'Status', 'CPU', 'Memory'], patterns=patterns)
    print(table)


if __name__ == '__main__':
    # url = 'http://localhost:8080/servers'
    server_ip = 'http://localhost:8080/'
    url = server_ip + 'servers'
    server_list = poll_for_server_list(url)
    # print (server_list)
    poll_for_detailed_server_info(server_list, server_ip)
    low_healthy_service_check()
    pretty_print()
    Server.objects.delete()
