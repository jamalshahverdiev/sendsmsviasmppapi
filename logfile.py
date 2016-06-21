#!/usr/bin/env python

import os
import numpy as np
import re

#p = os.popen('cat '+os.getcwd()+'/logfromkiwi.log | awk \'{ print $4,$24,$25,$26,$27 }\'',"r")
#count = 1
#while 1:
#    line = p.readline().strip()
#    if not line: 
#        break
#    print(line, count)
#    print(line)
#    count = count + 1

with open(os.getcwd()+'/logfromkiwi.log', 'r+') as logfile:
    for line in logfile.readlines():
        struct = re.split(r'[\s]\s*', line)
        #result = (struct[3], struct[23], struct[24], struct[25], struct[26])
        result = (struct[5], 'Int '+struct[16][-4:], struct[24])
        ctuptoline = ' '.join(result)
        with open('outofkiwilog.log', 'a') as out:
            out.write(ctuptoline)
            out.write('\n')
ctupline = open('outofkiwilog.log', 'r')
print(ctupline.read())

#os.system('cat outofkiwilog.log')

#clearfile = open('outofkiwilog.log', 'w')
#clearfile.seek(0)
#clearfile.truncate()
