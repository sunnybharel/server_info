# server_info
Poll Servers and present a basic CPU/RAM report and some stats.
Presents report in following fashion:
- Full view of all server IPs, CPU, RAM, Services and Health Status.
- Presents a report of servers grouped by type of Service and an aggregate of the CPU and RAM utilisation for that service.
- A view of any services running less than 2 healthy nodes (blank if no matches)

## Pre-requisites
- Run cpx_server script on port 8080 on localhost.
`
python cpx_server.py 8080
`

- Install pandas
- Ensure you have PyCurl, IO, json and re packages available. For example, to install PyCurl, see below:
`
pip install pycurl
`
## Usage
`
python server_info.py
`

