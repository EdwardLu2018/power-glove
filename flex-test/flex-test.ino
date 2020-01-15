#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();


void setup() {
  Serial.begin(9600);
  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  mma.setRange(MMA8451_RANGE_2_G);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
}

void loop() {
  Serial.print(analogRead(A0));
  Serial.print(" ");
  Serial.print(analogRead(A1));
  Serial.print(" ");
  Serial.print(analogRead(A2));
  Serial.print(" ");
  Serial.print(analogRead(A3));
  Serial.print(" ");
  Serial.print(analogRead(A4));
  Serial.print(" ");

  mma.read();
  Serial.print(mma.x); 
  Serial.print(" ");
  Serial.print(mma.y); 
  Serial.print(" ");
  Serial.print(mma.z);
  Serial.print(" "); 
  Serial.print(mma.getOrientation()); 
  Serial.println();

  /* Get a new sensor event */ 
  sensors_event_t event; 
  mma.getEvent(&event);

  delay(100);
}
