const mqtt = require('mqtt');

const client = mqtt.connect('mqtt://broker.hivemq.com'); // Replace with your MQTT broker URL

client.on('connect', function () {
  console.log('MQTT client connected');

  // Subscribe to the topic
  client.subscribe('dlaw4608/home/prediction/person', function (err) {
    if (err) {
      console.error('Error while subscribing to topic:', err);
    } else {
      console.log('Subscribed to topic');
    }
  });
});

client.on('message', function (topic, message) {
  console.log('Received message:', message.toString());
});

client.on('error', function (error) {
  console.log('MQTT error:', error.message);
});

client.on('close', function () {
  console.log('MQTT client disconnected');
});
