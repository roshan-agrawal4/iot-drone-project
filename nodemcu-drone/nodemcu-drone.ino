#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker


// WiFi
// Make sure to update this for your own WiFi network!
const char* ssid = "OnePlus7Pro";
const char* wifi_password = "Alright10";
double lat = 28.3588; 
double longi = 75.5880;
//for secure connection
const char* username = "drone";
const char* password = "drone123";
//ultrasonic variables
const int trigPin = D5;   
 const int echoPin = D6;   
 long duration;  
 double distance=100; 
 int flag = 1;
 double prev = 100.0;


// MQTT
// Make sure to update this for your own MQTT Broker!
const char* mqtt_server = "192.168.195.12";
const char* mqtt_topic = "test";
// The client id identifies the ESP8266 device. Think of it a bit like a hostname (Or just a name, like Greg).
const char* clientID = "client-one";


// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

void setup() {
  //for ultrasonic
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output  
 pinMode(echoPin, INPUT); // Sets the echoPin as an Input  

  // Begin Serial on 115200
  // Remember to choose the correct Baudrate on the Serial monitor!
  // This is just for debugging purposes
  Serial.begin(115200);

  Serial.print("Connecting to ");
  //Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  if (client.connect(clientID, username, password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
  
}

void loop() {

  //ultrasonic
   digitalWrite(trigPin, LOW);  
 delayMicroseconds(2);  
 // Sets the trigPin on HIGH state for 10 micro seconds  
 digitalWrite(trigPin, HIGH);  
 delayMicroseconds(10);  
 digitalWrite(trigPin, LOW);  
 // Reads the echoPin, returns the sound wave travel time in microseconds  
 duration = pulseIn(echoPin, HIGH);  
 // Calculating the distance  
 distance= duration*0.034/2.0;
 if (distance > 400.0 && flag){
  flag = 0;
  distance = 100;  
 }
 if (distance < 400){
  prev = distance;
 }
 
 if (distance > 400) {
  distance = prev;
 }
 // Prints the distance on the Serial Monitor  
 Serial.print("Distance: ");  
 Serial.println(distance);  
 
//gps code
  char output1[50];
  char output2[50];
  char output3[50];
  char out[50];
  char space[] = " ";

  snprintf(output1, 50, "%f", lat);
  snprintf(output2, 50, "%f", longi);
  snprintf(output3, 50, "%f", distance);
  strcat(output1, space);
  strcat(output1, output2);
  strcat(output1, space);
  strcat(output1, output3);

  //float longi = strtod(longitudes, longitude);
  ////snprintf(end, 50, "%f", number);
  Serial.println(output1);

  //client.publish(mqtt_topic, end);
  client.publish(mqtt_topic, output1);
  //client.publish(mqtt_topic, output2);
  lat = lat+0.0001;
  longi = longi+0.0001;
  //lat = lat+1;
  //longi = longi+1;
  //snprintf(latitude, 50, "%f", lat);
  //snprintf(longitude, 50, "%f", longi);
  delay(1000);
}