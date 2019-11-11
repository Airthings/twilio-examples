from twilio.rest import Client

class TwilioSMSAccount:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, message, number_from, number_to):
        self.client.messages.create(
            to=number_to, 
            from_=number_from,
            body=message)