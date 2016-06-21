Firstly poster.py script will read logfromsyslog.log file from Syslog server. After parsing logs it will replace needed things in post.xml file and send this XML file to SMS(SMPP) server via API. Phone numbers for team members we must write in post.xml file between body tags.

winposter.py file does same thing for Windows (Python2.7 installed ) server.
