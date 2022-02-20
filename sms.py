from twilio.rest import Client

def send_msg(phone, msg):
    account_sid = 'your-twilio-id'
    auth_token = 'your-auth'
    client = Client(account_sid, auth_token)
    message = client.messages.create (
            body=msg,
            from_='your-twilio-num',
            to='+1'+phone
            )


