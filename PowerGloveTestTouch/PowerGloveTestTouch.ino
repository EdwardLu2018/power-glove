/* FSR simple testing sketch.  <br>Connect one end of FSR to power, the other end to Analog 0.
Then connect one end of a 10K resistor from Analog 0 to ground 
*/


int fsrPin = 0;     // the FSR and 10K pulldown are connected to a0
int fsrReading;     // the analog reading from the FSR resistor divider

void setup(void) {
  Serial.begin(9600);  

}
 
void loop(void) {
  fsrReading = analogRead(fsrPin);  
 
  Serial.print("Analog reading = ");
  Serial.print(fsrReading);     // the raw analog reading
 
 
  if (fsrReading == 0) {
    Serial.println(" - No pressure");
  } else {
    Serial.println(" - touch");

  }
  delay(100);
}
