# Import smtplib for our actual email sending function
import smtplib

# Helper email modules
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# sender email address
email_user = 'hemllo.chatting.app@gmail.com'

# sender email passowrd for login purposes
email_password = 'Hemllo@2021'


def send_email(email_send="Error", body="Error", subject="OTP for Registrations on Hemllo Chatting App"):
    # list of users to whom email is to be sent
    # email_send = ['khemchand5487@gmail.com', 'jagram5487@gmail.com']
    msg = MIMEMultipart()
    msg['From'] = email_user

    # converting list of recipients into comma separated string
    msg['To'] = email_send
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    print("msg send")
    server.quit()


# send('khemchand5487@gmail.com', 'This is a test')
