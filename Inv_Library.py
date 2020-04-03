
import smtplib
"""it uses SMTP(Simmple Mail Transfer Protocol) to send email,
It creates SMTP client session objects for mailing. SMTP needs
valid source and destination email ids, and port numbers. 
for Google port is 587"""


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})'


def validate_email(email_id):
	if(re.search(email_regex, email_id)):
		return True
	else:
		return False


class EmailCred:
	def __init__(self, sender_add, sender_pass):
		self.sender_add = sender_add
		self.sender_pass = sender_pass

	def send_email(self, subject, receiver_address, mail_content):
		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = self.sender_add
		message['To']   = receiver_address
		message['Subject'] = subject
		#The body and the attachments for the mail
		message.attach(MIMEText(mail_content, 'plain'))
		#Create SMTP session for sending the mail
		session = smtplib.SMTP('smtp.gmail.com', 587)  #Use gmail with port
		session.starttls()	#Enable Security	
		#Login to the account with mail id and password
		try:
			session.login(self.sender_add, self.sender_pass)
		except:
			print("Failed")
			return False
		text = message.as_string()
		if( validate_email(receiver_address)):
			session.sendmail(self.sender_add, receiver_address, text)
			print('Mail Sent')
			session.quit()
			return True
		else:
			print("Invalid Email ID")
			return False
		
		

