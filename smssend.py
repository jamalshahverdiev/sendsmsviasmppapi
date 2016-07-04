#!/usr/bin/env python

import os
import datetime
import jinja2
import requests
#import re
import sys

now = datetime.datetime.now()
datetimerep = now.strftime("%Y-%m-%d %H:%M")
codepath = os.path.dirname(__file__)
outputdir = codepath+'/output/'

templateLoader = jinja2.FileSystemLoader( searchpath="/" )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPPFILE = codepath+'/post.xml'

tempp = templateEnv.get_template( TEMPPFILE )

NOTIFICATIONTYPE = sys.argv[1]
HOSTALIAS = sys.argv[2]
SERVICEDESC = sys.argv[3]
SERVICESTATE = sys.argv[4]

with open(outputdir+'cidfile', 'r+') as cidfile:
    cnt=(int(cidfile.read())+1)
    cidfile.seek(0)
    cidfile.truncate()
    cidfile.write(str(cnt))

smsline = ("** "+NOTIFICATIONTYPE+" Service Alert: "+HOSTALIAS+"/"+SERVICEDESC+" is "+SERVICESTATE+" **")
with open(outputdir+'outofsyslog.log', 'w') as out:
    out.write(smsline)
    out.write('\n')

cid = open(outputdir+'cidfile', 'r')
messages = open(outputdir+'outofsyslog.log', 'r')
ctuptoline = messages.read()
temppVars = { "datetimerep" : datetimerep, "cid" : cid.read(), "message" : ctuptoline, }
cid.close()
messages.close()
outputpText = tempp.render( temppVars )
with open(outputdir+'sendpost.xml', 'wb') as sendpost:
    sendpost.write(outputpText)

with open(outputdir+'sendpost.xml', 'r+') as filesendpost:
    data = filesendpost.read()
    headers = {'content-type': 'text/xml'}
    smpp_url = "http://sms.atltech.az:8080/bulksms/api"
    r = requests.post(smpp_url, data, headers=headers)
    with open(outputdir+'poststatus', 'wb') as poststatus:
        poststatus.write(str(r)+'\n')
        poststatus.write(str(r.content)+'\n')
    filesendpost.seek(0)
    filesendpost.truncate()
