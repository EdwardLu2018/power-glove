#include "keys.h"

/* Keyboard report buffer */
uint8_t buf[8] = { 0 };

void setup() {
  Serial.begin(9600);
}

void loop() {
  mouseKeys();
  delay(5000);
}

void mouseKeys() {
  for (int i = 0; i < 5; i++) {
    delay(10);
    buf[0] = 0;
    buf[2] = KEY_LEFTALT;
    Serial.write(buf, 8);
    releaseKey();
  }
}

void swipeRight() {
  buf[0] = 0;
  buf[2] = KEY_LEFTCTRL;
  Serial.write(buf, 8);
  delay(100);
  buf[0] = 0;
  buf[2] = KEY_LEFT; 
  Serial.write(buf, 8);
  releaseKey();
}

void swipeLeft() {
  buf[0] = 0;
  buf[2] = KEY_LEFTCTRL; 
  Serial.write(buf, 8);
  delay(100);
  buf[0] = 0;
  buf[2] = KEY_RIGHT; 
  Serial.write(buf, 8);
  releaseKey();
}

void releaseKey()
{
  buf[0] = 0;
  buf[2] = 0;
  Serial.write(buf, 8); // Release key
}
