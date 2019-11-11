# /usr/bin/env python
import json
from flask import Flask, request, abort
from twilioPython import TwilioSMSAccount

app = Flask(__name__)

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_NUMBER_FROM = ""
TWILIO_NUMBER_TO = ""
with open('config.json', 'r') as f:
    config_variables = json.load(f)
    TWILIO_ACCOUNT_SID = config_variables['accountSid']
    TWILIO_AUTH_TOKEN = config_variables['auth_token']
    TWILIO_NUMBER_FROM = config_variables['number_from']
    TWILIO_NUMBER_TO = config_variables['number_to']

# Setup Twilio account
twilioAccount = TwilioSMSAccount(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def print_devices(devices):
    allDevices = ''
    for device in devices:
        allDevices = allDevices + device + '\n'
    return allDevices


@app.route("/airthings-webhook", methods=['POST'])
def airthings_reply():
    """Respond to incoming Airthings measurements"""
    if request.method == 'POST':
        devices = []
        for device in request.json['data']:
            if device['radonShortTermAvg'] >= 50.0:
                devices.append(device['serialNumber'])
        if devices:
            twilioAccount.send_sms(
                number_to=TWILIO_NUMBER_TO, 
                number_from=TWILIO_NUMBER_FROM, 
                message='ALERT: Radon levels are above 50 becquerels in the following devices: \n' + print_devices(devices))
        return '', 200
    else:
        abort(400)

if __name__ == "__main__":
    app.run(debug=True, port=3000)