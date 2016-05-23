#!/usr/bin/env python

import pigpio
import email, imaplib, os, subprocess, smtplib

pi = pigpio.pi()
pi.set_PWM_frequency(14, 50)


detach_dir = "/home/ubuntu/foundersPrinting/files"

f = open('userConfig.txt', 'r')

user = f.readline().strip()
pwd = f.readline().strip()

smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtp.login(user, pwd)
m = imaplib.IMAP4_SSL('imap.gmail.com')
m.login(user,pwd)
m.select('Inbox')
resp, items = m.search(None, "(BODY 'confirm')", "(UNSEEN)")
items = items[0].split()

for emailid in items: # Iterates through email messages
	copies = 1
	doubleOption = ""
	foundOptions = False
	resp, data = m.fetch(emailid, "(RFC822)")
	email_body = data[0][1]
	mail = email.message_from_string(email_body)
	origSender = mail["From"]
	if mail.get_content_maintype() != 'multipart': # If the message doesn't have multiple parts, it can't have an attachment
		continue
	
	for part in mail.walk(): # Step through each part of the message
		
		if part.get_content_maintype() == 'text' and not foundOptions: # If it's the plaintext part, the main body, check for any options
			print "body"
			foundOptions = True
			body = part.get_payload(decode=True).lower()
			if "off" in body:
								pi.set_PWM_dutycycle(14, 0)
			elif "on" in body:
								pi.set_PWM_dutycycle(14, 255)
				continue
		
		if part.get_content_maintype() == 'multipart': # if it's still a multipart, ignore it
			continue
		
		if part.get('Content-Disposition') is None:
			continue
	

	m.store(emailid, '+FLAGS', '\Seen')
m.logout()

