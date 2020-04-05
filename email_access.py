



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


if (validate_email(sender_address)):
	new_email = EmailCred(sender_address, sender_pass)
	print(new_email.check_new_mail())
else:
	print("Invalid Email Account")



