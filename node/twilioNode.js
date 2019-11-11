const config = require('./config.json');
const accountSid = config.accountSid;
const authToken = config.auth_token;
const client = require('twilio')(accountSid, authToken);

module.exports = {
	twilioAccount: (message) => {
	client.messages
  .create({
     body: message,
     from: config.number_from,
     to: config.number_to
   })
  .then(message => console.log(message.sid));
}
};
