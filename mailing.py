from app import app
from flask_mail import Mail, Message
from variables import MAIL_SERVER,MAIL_PORT,MAIL_USERNAME,MAIL_PASSWORD,MAIL_USE_TLS,MAIL_USE_SSL,mail_smtp,mail_port
from secrets_key import mailing_email,mailing_password

mail= Mail(app)

app.config[MAIL_SERVER] = mail_smtp
app.config[MAIL_PORT] = mail_port
app.config[MAIL_USERNAME] = mailing_email
app.config[MAIL_PASSWORD] = mailing_password
app.config[MAIL_USE_TLS] = False
app.config[MAIL_USE_SSL] = True

mail= Mail(app)

def send_message(sender,recipients,subject,message_body=None,message_html=None,attachments=None):

    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = message_body
    msg.html = message_html
    msg.attachments = attachments

    try:
            mail.send(msg)
    except:
            return False
    return True