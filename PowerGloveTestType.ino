int fsrPin = 0;     // the FSR and 10K pulldown are connected to a0
int fsrReading; 
int randomChar = 0;// the analog reading from the FSR resistor divider

uint8_t buf[8] = { 
  0 };   /* Keyboard report buffer */

void setup() 
{
  Serial.begin(9600);
  delay(200);
}

void loop() 
{
  fsrReading = digitalabcdefghijklmnopqrstuvwxyz1234567890
   -=[]\\;'`,./Read(fsrPin);
  
  if (fsrReading != 0){
    randomChar = randomChar + 1;
    delay(100);
    buf[2] = randomChar;    // Random character
    Serial.write(buf, 8); // Send keypress
    releaseKey();
    if (randomChar == 26){
      randomChar = 0;
      }
  }

}

void releaseKey() 
{
  buf[0] = 0;
  buf[2] = 0;
  Serial.write(buf, 8); // Release key  
}
