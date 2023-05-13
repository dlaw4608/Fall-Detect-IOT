import paho.mqtt.client as mqtt
import json
from email.message import EmailMessage
import smtplib
import ssl
import time
from make_call import make_call  # importing the make_call function from another file

# MQTT broker settings
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "dlaw4608/home/prediction/person"
# Email settings
email_sender = 'standfallwatch123@gmail.com'
email_password = "sguxfhwqgkyyjcwn"
email_receiver = "yabovaf468@asuflex.com"
fallen_time = None
context = ssl.create_default_context()

def on_connect(client, userdata, flags, rc):
    """
    The function is called when the client has successfully connected to the broker.
    It subscribes to the topic and prints a message with the connection status.
    """
    print("Connected to MQTT broker" + str(rc))
    client.subscribe(mqtt_topic)


last_class_name = None

def on_message(client, userdata, msg):
    """
    The function is called when a message is received on the subscribed topic.
    It parses the message and checks if a person has fallen or is standing.
    If a person has fallen, it sends an email and makes a call.
    """
    global fallen_time, fallen_count, last_class_name
    print("Received message from topic: " + msg.payload.decode())
    jsonString = msg.payload.decode()
    prediction = json.loads(jsonString)
    class_name = prediction["predictions"][0]["class"]
    confidence = prediction["predictions"][0]["confidence"]
    if class_name == "Fallen_Human":
        if fallen_time is None:  # first fallen_human
            fallen_time = time.time()
            send_email("Warning: Someone has fallen!", f"Someone has fallen with {confidence} confidence.")
        elif last_class_name == "Fallen_Human":  # second fallen_human
            send_email("Warning: Fallen human showing no signs of getting up", 
                       "The fallen person has still not gotten up. Prepare for call from Fall Watch.")
            make_call() # call the make_call() function
            fallen_time = None
        last_class_name = "Fallen_Human"
    elif class_name == "Standing_Human":
        if fallen_time is not None:
            send_email("False alarm, the person is standing", f"The person is standing again with {confidence} confidence.")
            fallen_time = None
        last_class_name = "Standing_Human"



def send_email(subject, body):
    """
    The function sends an email with the given subject and body to the receiver email.
    It uses the Gmail SMTP server with SSL for secure communication.
    """
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


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()
