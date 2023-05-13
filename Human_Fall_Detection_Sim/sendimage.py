import paho.mqtt.client as mqtt
import json
from email.message import EmailMessage
import smtplib
import ssl

# MQTT broker settings
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "dlaw4608/home/predictions/real_motion"

email_sender = 'standfallwatch123@gmail.com'
email_password = "sguxfhwqgkyyjcwn"
email_receiver = "hodig77818@larland.com"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver

context = ssl.create_default_context()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())
    jsonString = msg.payload.decode()
    prediction = json.loads(jsonString)
    confidence = prediction["predictions"][0]["confidence"]
    human_stance = prediction["predictions"][0]["class"]
    if confidence > 0.75:
        send_email(human_stance, confidence)

def send_email(human_stance, confidence):
    # Update email subject and body based on fallen_human
    try:
        if human_stance == "Fallen_Human":
            subject = "Hey, there's someone fallen!"
            body = f"Someone has fallen with {confidence} confidence"
        elif human_stance == "Standing_Human":
            subject = "No need to be alarmed"
            body = f"The person is standing with {confidence} confidence"
        else:
            subject = "Unknown class detected"
            body = f"The detected class is {human_stance} with {confidence} confidence"

        em['Subject'] = subject
        em.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email: " + str(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

client.loop_forever()
