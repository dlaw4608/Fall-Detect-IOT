# Fall-Watch
IOT Standards and Protocols Assignment
By Daniel Lawton 


This is a project that utilises an object detectiom model to make predicitons on the postion of a person (standing/fallen). The Model used is called YOLOv5(OBB) and was trained using the web service RoboFLow, once the model was trained, it was applied to a roboflow API to make predicitons on images of people standing and fallen(prone). When the api made the appropriate predicitons these were then publioshed to an MQTT broker that had and notificstion script subsribed to the same topic. This script would take in the predicitons and depending on whether the predicitons were Standing_Human or Fallen_Human it would send notifications by email and call(Twilio).

