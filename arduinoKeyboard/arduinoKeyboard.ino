#include <SoftwareSerial.h>
#include "keys.h"

SoftwareSerial jetsonSerial (2, 3); // RX, TX

/* Keyboard report buffer */
uint8_t buf[8] = { 0 };

int mode = 0; //0 gesture, 1 mouse, 2 keyboard 

void setup() {
  Serial.begin(9600);
  jetsonSerial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop() {
  if (jetsonSerial.available()) {
    byte in = jetsonSerial.read();
    if ((in < 8) && (mode != 1)) { //if recieving a gesture and not in mouse mode - imply switch to gesture mode
      mode = 0;
    }
    switch(in) {
      case 0: swipeRight(); break;
      case 1: swipeLeft(); break;
      case 2: minWindow(); break;
      case 3: up(); break;
      case 4: down(); break;
      case 5: enableMouse(); break;
      //Sophia's adding more gestures
      case 6: openChrome(); break;
      case 7: closeWindow(); break;
      case 129: showAllWin(); break;
      case 130: faceTime(); break;
      case 131: iTunes(); break;
      case 132: enter(); break;
      case 133: volumeUp(); break;
      case 134: volumeDown(); break;
      default: keyboardEntry(in); break;
    }
  }
}

void keyboardEntry(byte in) {
  char ch = (char)in;
  if ((ch < 8) || (ch > 127)) {
    return;
  }

  //capitalize and write uppercase letters
  byte to_write = 0;
  if ((ch >= 65) && (ch <= 90)) {
    buf[0] = 0;
    buf[2] = KEY_MOD_LSHIFT;
    Serial.write(buf, 8);
    delay(10);
    ch = ch - 61;
    to_write = (byte)ch;
    buf[0] = 0;
    buf[2] = to_write;
    Serial.write(buf, 8);
    delay(10);
    releaseKey();
  }
  else if ((ch >= 97) && (ch <= 122)) {
    ch = ch - 93;
    to_write = (byte)ch;
    buf[0] = 0;
    buf[2] = to_write;
    Serial.write(buf, 8);
    delay(10);
    releaseKey();
  } else {
    if (ch == 10) {
      buf[0] = 0;
      buf[2] = KEY_ENTER;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 32) {
      buf[0] = 0;
      buf[2] = KEY_SPACE;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 8) {
      buf[0] = 0;
      buf[2] = KEY_BACKSPACE;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 27) {
      buf[0] = 0;
      buf[2] = KEY_ESC;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 46) {
      buf[0] = 0;
      buf[2] = KEY_DOT;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 44) {
      buf[0] = 0;
      buf[2] = KEY_COMMA;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 47) {
      buf[0] = 0;
      buf[2] = KEY_SLASH;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 60) {
      buf[0] = 0;
      buf[2] = KEY_MOD_LSHIFT;
      Serial.write(buf, 8);
      delay(10);
      buf[0] = 0;
      buf[2] = KEY_COMMA;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 62) {
      buf[0] = 0;
      buf[2] = KEY_MOD_LSHIFT;
      Serial.write(buf, 8);
      delay(10);
      buf[0] = 0;
      buf[2] = KEY_DOT;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 63) {
      buf[0] = 0;
      buf[2] = KEY_MOD_LSHIFT;
      Serial.write(buf, 8);
      delay(10);
      buf[0] = 0;
      buf[2] = KEY_SLASH;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 59) {
      buf[0] = 0;
      buf[2] = KEY_SEMICOLON;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
    }
    if (ch == 58) {
      buf[0] = 0;
      buf[2] = KEY_MOD_LSHIFT;
      Serial.write(buf, 8);
      delay(10);
      buf[0] = 0;
      buf[2] = KEY_SEMICOLON;
      Serial.write(buf, 8);
      delay(10);
      releaseKey();
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
  if (mode != 1) { //switch into mouse mode 
    mode = 1;
  } else { //switch into keyboard mode 
    mode = 2;
  }
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

void openChrome(){
  buf[0] = 0;
  buf[2] = KEY_LEFTMETA; 
  Serial.write(buf, 8);
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_SPACE; 
  Serial.write(buf, 8);
  releaseKey();
  //CHROME
  buf[0] = 0;
  buf[2] = KEY_C; 
  Serial.write(buf, 8);
  delay(10);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_H; 
  Serial.write(buf, 8);
  delay(10);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_R; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_O; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_M; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_E; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_ENTER; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  }

//Command Q
void closeWindow(){
  buf[0] = 0;
  buf[2] = KEY_LEFTMETA; 
  Serial.write(buf, 8);
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_Q; 
  Serial.write(buf, 8);
  releaseKey();
  }

//Control Down
void showAllWin(){
  buf[0] = 0;
  buf[2] = KEY_LEFTCTRL; 
  Serial.write(buf, 8);
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_DOWN; 
  Serial.write(buf, 8);
  releaseKey();
  }

//Command Space bar then type faceTime
void faceTime(){
  buf[0] = 0;
  buf[2] = KEY_LEFTMETA; 
  Serial.write(buf, 8);
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_SPACE; 
  Serial.write(buf, 8);
  releaseKey();
  //CHROME
  buf[0] = 0;
  buf[2] = KEY_F; 
  Serial.write(buf, 8);
  delay(10);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_A; 
  Serial.write(buf, 8);
  delay(10);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_C; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_E; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_T; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_I; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_M; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_E; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_ENTER; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  }
  
//Command Space bar then type iTunes
void iTunes(){
  buf[0] = 0;
  buf[2] = KEY_LEFTMETA; 
  Serial.write(buf, 8);
  delay(10);
  buf[0] = 0;
  buf[2] = KEY_SPACE; 
  Serial.write(buf, 8);
  releaseKey();
  //CHROME
  buf[0] = 0;
  buf[2] = KEY_I; 
  Serial.write(buf, 8);
  delay(10);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_T; 
  Serial.write(buf, 8);
  delay(10);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_U; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_N; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_E; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_S; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  buf[0] = 0;
  buf[2] = KEY_ENTER; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  }
void enter() {
  buf[0] = 0;
  buf[2] = KEY_ENTER; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
  }

void volumeUp() {
  buf[0] = 0;
  buf[2] = KEY_MEDIA_VOLUMEUP; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
}

void volumeDown() {
  buf[0] = 0;
  buf[2] = KEY_MEDIA_VOLUMEDOWN; 
  delay(10);
  Serial.write(buf, 8);
  releaseKey();
}
  
void releaseKey() {
  buf[0] = 0;
  buf[2] = KEY_NONE; // Release key
  Serial.write(buf, 8); 
}
