"""
Python MQTT Subscription client - No Username/Password
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
from firebase import firebase
import datetime;

mydb = firebase.FirebaseApplication('https://drone-system-iot-default-rtdb.firebaseio.com/', None)
# Don't forget to change the variables for the MQTT broker!
mqtt_username = "drone"
mqtt_password = "drone123"
mqtt_topic = "test"
mqtt_broker_ip = "169.254.39.31"


client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print("Connected!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
coord=["28.3588", "0", "100"]
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    dat=str((msg.payload).decode())
    
    coord=dat.split()
    ct = datetime.datetime.now()
    #long=str(msg.payload)
    #print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    print("\nLatitude: " + coord[0] + " Longitude: "+ coord[1]+ " Obstacle dist: "+ coord[2]+" timestamp:"+ str(ct))
    data2 = {"Latitude": coord[0], "Longitude": coord[1], "timestamp": str(ct)}
    data3={"Obst_dist": coord[2], "timestamp": str(ct)}
    
    mydb.post('/gps', data2)
    mydb.post('/ultrasonic', data3)
    #print("Hello")
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run


def main():
    client.on_connect = on_connect
    client.on_message = on_message
    #data = {"Temperature": 300, "Humidity": 40}
    #mydb.post('/sensor/gps', data)
    

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
    client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
    client.loop_forever()
    mqtt_client.loop_start() 

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()


