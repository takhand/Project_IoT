#include <SoftwareSerial.h>
#include <aJSON.h>
//SoftwareSerial mySerial(0, 1); // RX, TX

char response;



unsigned long current; 

void setup() {
   Serial.begin(9600);
//   mySerial.begin(9600);
}

void loop(){
  
   
 current = millis();
   do {
      response = Serial.read();
      if ((millis()-current) > 2000) break; 
      
   }while (response == -1); 
   
   Serial.println(response);
   
}
