#! python

import os
import datetime
import jinja2
import requests

now = datetime.datetime.now()
datetimerep = now.strftime("%Y-%m-%d %H:%M")

templateLoader = jinja2.FileSystemLoader(searchpath="C:\\Pysmssender")

templateEnv = jinja2.Environment( loader=templateLoader )
TEMPPFILE = 'post.xml'

tempp = templateEnv.get_template( TEMPPFILE )

with open('\Pysmssender\output\cidfile', 'r+') as cidfile:
    cnt=(int(cidfile.read())+1)
    cidfile.seek(0)
    cidfile.truncate()
    cidfile.write(str(cnt))

cid = open('\Pysmssender\output\cidfile', 'r')
temppVars = { "datetimerep" : datetimerep, "cid" : cid.read(), }
cid.close()
outputpText = tempp.render( temppVars )

with open('\Pysmssender\output\sendpost.xml', 'wb') as sendpost:
    sendpost.write(outputpText)

with open('\Pysmssender\output\sendpost.xml', 'r') as filesendpost:
    data = filesendpost.read()
    headers = {'content-type': 'text/xml'}
    smpp_url = "http://sms.atltech.az:8080/bulksms/api"
    r = requests.post(smpp_url, data, headers=headers)
    print(r)
