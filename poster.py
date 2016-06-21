#!/usr/bin/env python

import os
import datetime
import jinja2
import requests
import re

now = datetime.datetime.now()
datetimerep = now.strftime("%Y-%m-%d %H:%M")

templateLoader = jinja2.FileSystemLoader( searchpath="/" )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPPFILE = os.getcwd()+'/post.xml'

tempp = templateEnv.get_template( TEMPPFILE )

with open(os.getcwd()+'/output/cidfile', 'r+') as cidfile:
    cnt=(int(cidfile.read())+1)
    cidfile.seek(0)
    cidfile.truncate()
    cidfile.write(str(cnt))

with open(os.getcwd()+'/logfromsyslog.log', 'r+') as logfile:
    for line in logfile.readlines():
        struct = re.split(r'[\s]\s*', line)
        result = (struct[5], struct[16], struct[24])
        handledline = ' '.join(result)
        with open(os.getcwd()+'/output/outofsyslog.log', 'a') as out:
            out.write(handledline)
            out.write('\n')
    logfile.seek(0)
    logfile.truncate()

cid = open(os.getcwd()+'/output/cidfile', 'r')
messages = open(os.getcwd()+'/output/outofsyslog.log', 'r')
ctuptoline = messages.read()
temppVars = { "datetimerep" : datetimerep, "cid" : cid.read(), "message" : ctuptoline, }
cid.close()
messages.close()
outputpText = tempp.render( temppVars )
with open(os.getcwd()+'/output/sendpost.xml', 'wb') as sendpost:
    sendpost.write(outputpText)

with open(os.getcwd()+'/output/sendpost.xml', 'r+') as filesendpost:
    data = filesendpost.read()
    headers = {'content-type': 'text/xml'}
    smpp_url = "http://sms.atltech.az:8080/bulksms/api"
    r = requests.post(smpp_url, data, headers=headers)
    print(r)
    filesendpost.seek(0)
    filesendpost.truncate()

clearfile = open(os.getcwd()+'/output/outofsyslog.log', 'w')
clearfile.seek(0)
clearfile.truncate()
