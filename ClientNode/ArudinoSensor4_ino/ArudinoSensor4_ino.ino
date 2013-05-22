//int pins[] = {0,1,2,3,4,5};

String c;
int temp;
//float temp2;
//char test[10];

unsigned long current; 
int response; 

void setup () {
   Serial.begin(9600);
}


void loop() {   
   String payload;
   delay(5000);
   
   temp = analogRead(0);
   delay(5);
   
   temp = analogRead(0);\
   delay(10);
   c = String(temp);
   payload = payload + c + ".";
   
   temp = analogRead(1);
   delay(10);
   c = String(temp);
   payload = payload + c + ".";
   
   temp = analogRead(2);
   delay(10);
   c = String(temp);
   payload = payload + c + ".";
   
   temp = analogRead(3);
   delay(10);
   c = String(temp);
   payload = payload + c + ".";
   
   Serial.println(payload); 
   
   current = millis(); 
   
   do {
      response = Serial.read();
      if ((millis()-current) > 5000) break; 
      
   }while (response == -1);
} 
