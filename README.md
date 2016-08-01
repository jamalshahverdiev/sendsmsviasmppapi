<html>
<meta charset="utf-8">
Firstly <b>poster.py</> script will read <b>logfromsyslog.log</> file from Syslog server. After parsing logs it will replace needed things in <b>post.xml</> file and send this XML file to SMS(SMPP) server via API. Phone numbers for team members we must write in post.xml file between body tags.

<b>winposter.py</b> file does same thing for Windows (Python2.7 installed ) server. 

<b>smssend.py</b> was written for Nagios monitoring station for send sms.
</html>
