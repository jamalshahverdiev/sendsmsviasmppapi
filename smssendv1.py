#!/usr/bin/env python

import os
import datetime
import time
import jinja2
import requests
import sys
import subprocess

oldtaskid = subprocess.check_output("cat output/poststatus | tail -n1 | awk -F  'taskid' '/2/ {print $2}' | tr -d '>,<,/'", shell=True)
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
smsline = ("** "+NOTIFICATIONTYPE+" Service Alert: "+HOSTALIAS+"/"+SERVICEDESC+" is "+SERVICESTATE+" **")

def cidplusone(outputdir):
    with open(outputdir+'cidfile', 'r+') as cidfile:
        cnt=(int(cidfile.read())+1)
        cidfile.seek(0)
        cidfile.truncate()
        cidfile.write(str(cnt))

with open(outputdir+'outofsyslog.log', 'w') as out:
    out.write(smsline)
    out.write('\n')

def mescreate(outputdir, datetimerep):
    messages = open(outputdir+'outofsyslog.log', 'r')
    ctuptoline = messages.read()
    messages.close()
    cid = open(outputdir+'cidfile', 'r')
    temppVars = { "datetimerep" : datetimerep, "cid" : cid.read(), "message" : ctuptoline, }
    cid.close()
    global outputpText
    outputpText = tempp.render( temppVars )

def tempcreate_and_send(outputdir,outputpText):
    with open(outputdir+'sendpost.xml', 'wb') as sendpost:
        sendpost.write(outputpText)
    
    with open(outputdir+'sendpost.xml', 'r+') as filesendpost:
        data = filesendpost.read()
        headers = {'content-type': 'text/xml'}
        smpp_url = "http://www.sendsms.az/smxml/api"
        r = requests.post(smpp_url, data, headers=headers)
        with open(outputdir+'poststatus', 'wb') as poststatus:
            poststatus.write(str(r)+'\n')
            poststatus.write(str(r.content)+'\n')
        filesendpost.seek(0)
        filesendpost.truncate()

cidplusone(outputdir)
mescreate(outputdir, datetimerep)
tempcreate_and_send(outputdir,outputpText)

time.sleep(60)
newtaskid = subprocess.check_output("cat output/poststatus | tail -n1 | awk -F  'taskid' '/2/ {print $2}' | tr -d '>,<,/'", shell=True)
while oldtaskid == newtaskid:
    cidplusone(outputdir)
    mescreate(outputdir, datetimerep)
    tempcreate_and_send(outputdir,outputpText)
    newtaskid = subprocess.check_output("cat output/poststatus | tail -n1 | awk -F  'taskid' '/2/ {print $2}' | tr -d '>,<,/'", shell=True)
else:
    sys.exit
