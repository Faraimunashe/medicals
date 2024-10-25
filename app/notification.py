from twilio.rest import Client
from flask_mail import Message
from . import mail

account_sid = 'ACb3fb519e3ceb5ddb3424e90fdc0ca876'
auth_token = '7bb573a83057caf443b8fd638b23979a'
from_number = '+12706122769'

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