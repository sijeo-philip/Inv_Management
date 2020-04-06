
import smtplib
"""it uses SMTP(Simmple Mail Transfer Protocol) to send email,
It creates SMTP client session objects for mailing. SMTP needs
valid source and destination email ids, and port numbers. 
for Google port is 587"""


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import email
import imaplib
from email.parser import BytesParser, Parser 
from email.policy import default
import os
import re
import sys

email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})'
email_dict = {}


def validate_email(email_id):
	if(re.search(email_regex, email_id)):
		return True
	else:
		return False


class EmailCred:
	def __init__(self, sender_add, sender_pass):
		self.sender_add = sender_add
		self.sender_pass = sender_pass
		self.osType = sys.platform
		if ( self.osType == 'win32' ):
			os.system('mkdir C:\\component_requests')
		elif ( self.osType == 'linux1' or self.osType == 'linux2'):
			os.system('mkdir \\home\\component_requests')

	def send_email(self, subject, receiver_address, mail_content,attachment=False):
		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = self.sender_add
		message['To']   = receiver_address
		message['Subject'] = subject
		#The body and the attachments for the mail
		message.attach(MIMEText(mail_content, 'plain'))
		#Create SMTP session for sending the mail
		if ( True == attachment ):
			if self.osType == 'win32':
				attach_file_dir = os.path.join("C:\\", "component_requests")
				attach_file_name = os.path.join(attach_file_dir, "component_requests.xlsx")
			elif (self.osType == 'linux1' or self.osType == 'linux2'):
				attach_file_dir = os.path.join("\\home\\", "component_requests")
				attach_file_name = os.path.join(attach_file_dir, "component_requests.xlsx")
			else:
				return False
			try:
				attachfile = open(attach_file_name, "rb")
				payload = MIMEBase('application', 'octet-stream')
				payload.set_payload(attachfile.read())
				attachfile.close()
			except Exception as e:
				print(e)
				return False


			encoders.encode_base64(payload)  #Encode the attachment
			#add payload header with filename
			payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
			message.attach(payload)

		session = smtplib.SMTP('smtp.gmail.com', 587)  #Use gmail with port
		session.starttls()	#Enable Security	
		#Login to the account with mail id and password
		try:
			session.login(self.sender_add, self.sender_pass)
		except:
			print("Failed")
			return False
		finally:
			text = message.as_string()
			if( validate_email(receiver_address)):
				session.sendmail(self.sender_add, receiver_address, text)
				print('Mail Sent')
				session.quit()
				return True
			else:
				print("Invalid Email ID")
				return False
		
	def check_new_mail(self):
		email_dict.clear()
		try:
			imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
			imap.login(self.sender_add, self. sender_pass)
			imap.select("INBOX")
			status , response = imap.search(None, '(UNSEEN)')
			unread_msg_nums = response[0].split()
			if len(unread_msg_nums) > 0 :
				for e_id in unread_msg_nums:
					_, response = imap.fetch(e_id, '(RFC822)')
					headers = Parser(policy=default).parsestr(response[0][1].decode("utf-8"))
					email_dict[e_id.decode()] = headers['from']

			imap.logout()
		except Exception as e:
			print(e)
			return email_dict

		return email_dict;

	def read_email(self, email_id):
		try:
			imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
			imap.login(self.sender_add, self.sender_pass)
			imap.select("INBOX")
			typ, data = imap.fetch(email_id, '(RFC822)')
			raw_email = data[0][1]
		except Exception as e:
			return e

       
		#converts byte literal to string removing b ''
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)

		#downloading attachements
		for msg in email_message.walk():
			if msg.get_content_maintype() == 'multipart':
				continue
			if msg.get('Content-Disposition') is None:
				continue
			fileName = msg.get_filename()

			if (bool(fileName) and (fileName == 'component_requests.xlsx')):
				if self.osType == 'win32':
					attach_file_dir = os.path.join("C:\\", "component_requests")
				elif (self.osType == 'linux1' or self.osType == 'linux2'):
					attach_file_dir = os.path.join("\\home\\", "component_requests")
				else:
					return "Not Compatible OS"
				attach_file_name = os.path.join(attach_file_dir, "component_requests.xlsx")
				with open(attach_file_name, 'wb' ) as f:
					f.write(msg.get_payload(decode=True))
				return "File Downloaded"
		return "No Attachment Found!"







		


