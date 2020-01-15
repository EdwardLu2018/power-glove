#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial); // wait for serial port to connect. Needed for Native USB only

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() // run over and over
{
  if (mySerial.available() > 0) {
    byte in = mySerial.read();
    if (in == '1') {
      digitalWrite(13, HIGH);
    }
    if (in == '2') {
      digitalWrite(13, LOW);
    }
  }
}
