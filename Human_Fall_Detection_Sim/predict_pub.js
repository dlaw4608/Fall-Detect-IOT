// Require necessary packages
const axios = require("axios");
const fs = require("fs");
const mqtt = require("mqtt");

// Connect to an MQTT broker
const client = mqtt.connect("mqtt://broker.hivemq.com"); 

// Read images and convert to base64 encoding
const image1 = fs.readFileSync("images/fallen_person.jpeg", { encoding: "base64" });
const image2 = fs.readFileSync("images/testconfidence.jpg", { encoding: "base64" });

// Function to detect a person in an image and publish the result to an MQTT topic
function detectPerson(image) {
  axios({
    method: "POST",
    url: "https://detect.roboflow.com/standing_falling/2", 
    params: {
      api_key: "sEiqCsLz4EzXjFsOHKKf" 
    },
    data: image, 
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  })
    .then(function(response) {
      const prediction = response.data;
      console.log("Person detection result:", prediction);
    
      client.publish("dlaw4608/home/prediction/person", JSON.stringify(prediction));
    })
    .catch(function(error) {
      console.log("Error while detecting person:", error.message);
    });
}

// When MQTT client is connected, detect person in the images after a delay
client.on("connect", function() {
  console.log("MQTT client connected");

  setTimeout(() => detectPerson(image1), 10000);
  setTimeout(() => detectPerson(image2), 20000);
});

// Log errors and disconnections
client.on("error", function(error) {
  console.log("MQTT error:", error.message);
});

client.on("close", function() {
  console.log("MQTT client disconnected");
});
