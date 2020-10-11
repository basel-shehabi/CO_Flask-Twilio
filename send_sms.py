import os

from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Make API calls here...
message = client.messages \
                .create(
                     messaging_service_sid='MGf228c23b6378caba1e8bc9b41ab07dad',
                     body='body',
                     to='+447838538545'
                 )

print(message.sid)
