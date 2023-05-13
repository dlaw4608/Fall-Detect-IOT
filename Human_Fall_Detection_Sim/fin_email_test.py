import paho.mqtt.client as mqtt
import json
from email.message import EmailMessage
import smtplib
import ssl
import time
from twilio.rest import Client

# MQTT broker settings
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "dlaw4608/home/prediction/person"

# Email settings
email_sender = 'standfallwatch123@gmail.com'
email_password = "sguxfhwqgkyyjcwn"
email_receiver = "yifixef821@andorem.com"

# Twilio settings
account_sid = 'AC0730b8042e56d8b50ce763a3e3b68de7'
auth_token = '9f48c555070acdfe68f8ca05232d00cb'
twilio_phone_number = '+16205318597'
my_phone_number = "+353857058967"

# Global variables
fallen_time = None
fallen_count = 0
last_class_name = None

context = ssl.create_default_context()


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker" + str(rc))
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    global fallen_time, fallen_count, last_class_name

    print("Received message from topic: " + msg.payload.decode())

    jsonString = msg.payload.decode()
    prediction = json.loads(jsonString)
    class_name = prediction["predictions"][0]["class"]
    confidence = prediction["predictions"][0]["confidence"]

    if class_name == "Fallen_Human":
        fallen_count += 1

        if fallen_time is None:
            fallen_time = time.time()

            send_email("Warning: Someone has fallen!", f"Someone has fallen with {confidence} confidence.")
            
        elif fallen_count == 2:
            send_email("Warning: Fallen human showing no signs of getting up", 
                       "The fallen person has still not gotten up. Prepare for call from Fall Watch.")
            time.sleep(5)
            make_call()

            fallen_time = None
            fallen_count = 0

        last_class_name = "Fallen_Human"

    elif class_name == "Standing_Human":
        if fallen_time is not None:
            send_email("False alarm, the person is standing", f"The person is standing again with {confidence} confidence.")
            fallen_time = None
            fallen_count = 0
        last_class_name = "Standing_Human"


def send_email(subject, body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver

    try:
        em['Subject'] = subject
        em.set_content(body)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        print("Email sent successfully")

    except Exception as e:
        print("Failed to send email: " + str(e))

def make_call():
    client = Client(account_sid, auth_token)
    try:
        call = client.calls.create(
            to=my_phone_number,
            from_=twilio_phone_number,
            url='http://demo.twilio.com/docs/voice.xml'
        )

        print("Phone call initiated.")
    except Exception as e:
        print("Failed to make call: " + str(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()
