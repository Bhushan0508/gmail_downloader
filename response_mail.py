import smtplib
from email.mime.text import MIMEText


smtp_username=''
smtp_password=''

# Sender information
sender_email = smtp_username
sender_password = smtp_password

# Recipient information
recipient_email = "bhushan0508@gmail.com"

# Subject and body of the reply

body = "Your reply message here..."

def reply(body,original_subject,sender_email,recipient_email,attachment_file):
    print('In reponse_mail.reply()')
    # Construct the email message
    subject = "Re: "+original_subject
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    # Connect to the mail server and send the email
    with smtplib.SMTP("smtp.google.com") as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
