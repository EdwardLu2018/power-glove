void setup() {
  Serial.begin(9600); // open the serial port at 9600 bps:
}

void loop() {
  // print labels
  Serial.print("1 2 3 4 5 6 7 8 9 10 11");  
  Serial.println();        // prints another carriage return
  delay(200);
}
