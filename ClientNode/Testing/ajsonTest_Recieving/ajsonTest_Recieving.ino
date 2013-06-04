#include <aJSON.h>
#include <SoftwareSerial.h> 

aJsonStream serial_stream(&Serial);

void setup() {
   Serial.begin(9600); 
}


void loop() {
   
