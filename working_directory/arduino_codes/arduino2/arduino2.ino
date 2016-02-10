#include<Servo.h>
int x,y,z;

float pick_val=45;
float place_val=140;
int vert_down_angle = 95;
int vert_up_angle = 140;
//change for adjustments

int rot_servo_pin=6;
int vert_servo_pin=5;
int hand_servo_pin=3;
//change on basis of connections

int comma=222;
int com_pick=200;
int com_place=211;
//one needs to be odd and the other even

Servo rot_servo;
Servo vert_servo;
Servo hand_servo;

void arm_sequence(float p,int s){
  float f;
  if(s==0){
    f=pick_val;
  }
  if(s==1){
    f=place_val;
  }
  rot_servo.write(p);
  digitalWrite(13,HIGH);
  delay(1000);
  vert_servo.write(vert_down_angle);
  digitalWrite(13,LOW);
  delay(1000);
  hand_servo.write(f);
  digitalWrite(13,HIGH);
  delay(1000);
  vert_servo.write(vert_up_angle);
  digitalWrite(13,LOW);
  delay(1000);
}

void setup(){
  Serial.begin(57600);
  rot_servo.attach(rot_servo_pin);
  vert_servo.attach(vert_servo_pin);
  hand_servo.attach(hand_servo_pin);
  vert_servo.write(vert_up_angle);
  pinMode(13,OUTPUT);
//  digitalWrite(13,LOW);
//  delay(1000);
//  digitalWrite(13,HIGH);
//  delay(1000);
//  digitalWrite(13,LOW);
//  delay(1000);
}

void loop(){
  if(Serial.available()==3){
    x= Serial.read();
    y= Serial.read();
    z= Serial.read();
    Serial.print(x);
    Serial.print(y);
    Serial.print(z);
    Serial.write('o');
    if(y==222 && (x==com_pick || x==com_place)){
      arm_sequence(z,x%2);
//      digitalWrite(13,HIGH);
//      delay(100);
//      digitalWrite(13,LOW);
//      delay(100);
    }
  }
}