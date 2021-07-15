#!/usr/bin/python

import smtplib

smtpServer = 'localhost'
sender = 'send@email.com'
receivers = ['EMAIL']
fromName = "sender"
toName = "receiver"
subject = "Test Email"
body = "This is a test email."

message = """From: """+fromName+""" <"""+sender+""">
To: """+toName+""" <"""+str(receivers[0])+""">
Subject: """+subject+"""

"""+body+"""
"""

try:
   smtpObj = smtplib.SMTP(smtpServer)
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except SMTPException:
   print("Error: unable to send email")