



from Inv_Library import EmailCred
from Inv_Library import validate_email


mail_content = '''Hello, This is a simple mail. there is only text, 
				  attachments are there the mail is send using Python
				  SMTP library Thank you '''

#The email address and password
sender_address  = 'unisem.components@gmail.com'
sender_pass		= 'unisem123'
receiver_address= 'sijeo80@gmail.com'
sub 			= 'Test Mail'

mail_str =''
sender_dict = {}
if (validate_email(sender_address)):
	new_email = EmailCred(sender_address, sender_pass)
	sender_dict = new_email.check_new_mail()
	print(sender_dict)
	for email_id, sender in sender_dict.items():
		mail_str = new_email.read_email(email_id)
		print("{} from {}".format(mail_str, sender))

else:
	print("Invalid Email Account")



