from twilio.rest import Client
from flask_mail import Message
from . import mail

account_sid = ''
auth_token = ''
from_number = ''

def send_sms():
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Fradulent transaction was detected",
        from_=from_number,
        to="+263783540959"
        #to="+263780518296"
    )

    print("SMS Message Sent:")




def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)