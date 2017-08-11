#!/usr/bin/python

#send email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import email.utils
import smtplib
import sys

# set UTF-8
default_encoding = 'utf-8'

fromaddr = "example@email.com"
password = "password"
toaddr = "toexample@email.com"
server = smtplib.SMTP('smtp.example.com', 25)

#set MIME
msg = MIMEMultipart()
msg['Subject'] = "Hello from the Author of Automate It!"
msg['To'] = email.utils.formataddr(('Recipient', toaddr))
msg['From'] = email.utils.formataddr(('Author',fromaddr))
body = "What a wonderful world!"
msgBody = MIMEText(body, 'plain')
msg.attach(msgBody)

#set attachment
filename = "attach.txt"
attachment = open(filename, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment;filename= %s" % filename)
msg.attach(part)

text = msg.as_string()

try:
    server.set_debuglevel(True)
    print ("Sending ehlo")
    server.ehlo()
    if server.has_extn('STARTTLS'):
        print ("Starting TLS Session")
        server.starttls()
        print ("Sending ehlo again")
        server.ehlo()

finally:
    server.login(fromaddr, password)
    server.sendmail(fromaddr, toaddr, text)
    server.quit()