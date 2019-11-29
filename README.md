# server_info
Poll Servers and present a basic CPU/RAM report

## Pre-requisites
- Docker instance running mongoDB
`
docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4
docker exec -it mongodb bash
`
Once in interactive bash mode type the following:
`mongo`
Once inside mongo terminal, pass the following commands to create a new DB
``
use server_db
db
`
The result of 'db' command should show 'server_db' implying that the new database we created is currently selected for use.
Now, exit the mongo shell and the docker interactive shell too.
Type 'exit' on each shell. You may have to do this twice to get back to your host machine's shell.

- Get pip to install mongoengine
`
pip install mongoengine
`
- Install pycurl
`
pip install pycurl
`


