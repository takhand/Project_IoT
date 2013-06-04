#include <aJSON.h> 
String c; 

char temp; 
int counter = 0; 
boolean take = false;
unsigned long current; 
String response = String(); 


void setup() {
   Serial.begin(9600); 
}

void loop() {
   //   Serial.println('waiting for packet'); 
   
   current = millis();
   do {
      temp = Serial.read();
      if (temp != -1){
         response.concat(String(temp));
      }
      if ((millis()-current) > 2000) break; 
   }while (temp == -1);
   
//   if (temp == '}') Serial.println('1');
//   Serial.println(temp);
   
   if(temp == ')') {
      Serial.println(response);
      take = false;
      response = String();
   }
}
