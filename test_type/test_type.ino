uint8_t buf[8] = { 0 }; /* Keyboard report buffer */

void setup()
{
  Serial.begin(9600);
  randomSeed(analogRead(0));
  delay(200);
}

void loop()
{
  delay(200);
  
  buf[0] = 0;
  buf[2] = 0xE0; // control
  Serial.write(buf, 8);
  delay(200);
  buf[0] = 0;
  buf[2] = 0x50; 
  Serial.write(buf, 8);
  releaseKey();
}
  
void releaseKey()
{
  buf[0] = 0;
  buf[2] = 0;
  Serial.write(buf, 8); // Release key
}
