'use strict';
const http = require('http');
const bodyParser = require('body-parser');
const express = require('express');
const app = express();
const twilio = require('./twilioNode');

app.set('view engine', 'ejs');
app.use(
	bodyParser.urlencoded({
		extended: true
	})
);
app.use(express.static('public'));
app.use(bodyParser.json());

app.post('/airthings-webhook', (req, res) => {
	let devices = [];
	for (let deviceinfo in req.body.data) {
		if (req.body.data[deviceinfo].radonShortTermAvg >= 0) {
			devices.push(req.body.data[deviceinfo].serialNumber);
		}
	}
	if (devices.length > 0) {
		twilio.twilioAccount(
			'ALERT: Radon levels are above 99 becquerels in the following devices:\n'
			+ devices.reduce((allDevices, device) => allDevices + device + '\n'),
		);
	}
	res.sendStatus(200);
});

http.createServer(app).listen(3000, () => {
	console.log('Express server listening on port 3000');
});
