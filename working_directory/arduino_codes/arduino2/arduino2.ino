void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  pinMode(A3,INPUT);
  pinMode(A4,INPUT);
  pinMode(3,OUTPUT);
  pinMode(2,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:


  int a3 = analogRead(A3);
  int a4 = analogRead(A4);
  Serial.print(a3);
  Serial.print("      ");
  Serial.println(a4);
  if(a3 < 512) {
    digitalWrite(2,HIGH);
  }
  else {
    digitalWrite(2,LOW);
  }
  
  if(a4 < 512) {
    digitalWrite(3,LOW);
  }
  else {
    digitalWrite(3,HIGH);
  }
}
