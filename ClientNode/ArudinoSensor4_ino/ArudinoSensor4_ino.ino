#include  <aJSON.h>

aJsonStream serial_stream(&Serial);

int src = 0002;
int dst = 1874;
char *app = "Smart Seating";
//float temp2;
//char test[10];

unsigned long current; 
int response; 

void setup () {
   Serial.begin(9600);
}

aJsonObject *createMessage() {
   aJsonObject *msg = aJson.createObject();

   int analogValues[6];

   //Unrolled forloop
   analogValues[0] = analogRead(0); delay(10);
   analogValues[1] = analogRead(1); delay(10);
   analogValues[2] = analogRead(2); delay(10);
   analogValues[3] = analogRead(3); delay(10);
   analogValues[4] = analogRead(4); delay(10);
   analogValues[5] = analogRead(5); delay(10);

   aJsonObject *analog = aJson.createIntArray(analogValues,6);
   aJsonObject *source = aJson.createItem(src);
   aJsonObject *destination = aJson.createItem(dst);
   aJsonObject *type = aJson.createItem(app);

   aJson.addItemToObject(msg, "Type", type);
   aJson.addItemToObject(msg, "Destination", destination);
   aJson.addItemToObject(msg, "Source", source);
   aJson.addItemToObject(msg, "Values", analog);
   
   return msg; 
}


void loop() {  
   
   aJsonObject *msg = createMessage();
   aJson.print(msg, &serial_stream); 
//   Serial.println();
   aJson.deleteItem(msg);
   
//   delay(2000);
   current = millis(); 

   do {
      response = Serial.read();
      if ((millis()-current) > 2000) break; 

   }while (response == -1);
}


