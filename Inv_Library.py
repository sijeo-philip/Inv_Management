
import smtplib
"""it uses SMTP(Simmple Mail Transfer Protocol) to send email,
It creates SMTP client session objects for mailing. SMTP needs
valid source and destination email ids, and port numbers. 
for Google port is 587"""


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
		session.login(self.sender_add, self.sender_pass)
		text = message.as_string()
		session.sendmail(self.sender_add, receiver_address, text)
		session.quit()
		print('Mail Sent')

