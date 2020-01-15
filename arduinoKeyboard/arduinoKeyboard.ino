#include <SoftwareSerial.h>
#include "keys.h"

SoftwareSerial jetsonSerial (2, 3); // RX, TX

/* Keyboard report buffer */
uint8_t buf[8] = { 0 };

void setup() {
  Serial.begin(9600);
  jetsonSerial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}

void loop() {
  if (jetsonSerial.available()) {
    byte in = jetsonSerial.read();
    switch(in) {
      case '0': swipeRight(); break;
      case '1': swipeLeft(); break;
      case '2': minWindow(); break;
      case '3': up(); break;
      case '4': down(); break;
      default: break;
    }
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

void enableMouse() {
  for (int i = 0; i < 5; i++) {
    delay(10);
    buf[0] = 0;
    buf[2] = KEY_LEFTALT;
    Serial.write(buf, 8);
    releaseKey();
  }
}

void minWindow() {
  buf[0] = 0;
  buf[2] = KEY_LEFTMETA; 
  Serial.write(buf, 8);
  delay(100);
  buf[0] = 0;
  buf[2] = KEY_M; 
  Serial.write(buf, 8);
  releaseKey();
}

void up() {
  buf[0] = 0;
  buf[2] = KEY_UP; 
  Serial.write(buf, 8);
  releaseKey();
}

void down() {
  buf[0] = 0;
  buf[2] = KEY_DOWN; 
  Serial.write(buf, 8);
  releaseKey();
}

void releaseKey() {
  buf[0] = 0;
  buf[2] = KEY_NONE; // Release key
  Serial.write(buf, 8); 
}
