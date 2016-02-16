#include<Servo.h>

//-------------- SERVO CALIBRATED POSITIONS ------------------ 
float gripper_servo_grab_angle=20;
float gripper_servo_release_angle=100;
int vertical_servo_down_angle = 80;
int vertical_servo_up_angle = 140;

int gripper_servo_initial_position = 90;
int vertical_servo_initial_position = 120;
int rotation_servo_initial_position = 90;
//-------------- SERVO PIN ATTACHMENTS --------------------
int vertical_servo_pin = 6;
int rotation_servo_pin = 5;
int gripper_servo_pin =  3;

//-------------- COMMUNICATION BYTES ------------------------
int start_byte = 255;  // "\xff"
int pick_command = 97; // "a"
int place_command= 98; // "b"
int move_command = 99; // "c"
int handshake_command = 104; //"h"

char OKAY_CHARACTER = 'O';
char DONE_CHARACTER = 'D';
char NOT_OKAY_CHARACTER = 'N';
char ARDUINO_NUMBER = '2';

int DELAY = 3000;

Servo rotation_servo;
Servo vertical_servo;
Servo gripper_servo;

int COUNT = 0;

void setup(){
  Serial.begin(57600);
  //attach
  rotation_servo.attach(rotation_servo_pin);
  vertical_servo.attach(vertical_servo_pin);
  gripper_servo.attach(gripper_servo_pin);

  //move servos to initial positions
  rotation_servo.write(rotation_servo_initial_position);
  vertical_servo.write(vertical_servo_initial_position);
  gripper_servo.write(gripper_servo_initial_position);

  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
}

void loop(){
  int _start_byte_ = 0;
  int command = 0;
  int parameter = 0;
  if(Serial.available() == 3) {
    _start_byte_ = Serial.read();
    command = Serial.read();
    parameter = Serial.read();
    
    if(_start_byte_ == start_byte) {
      _blink_();
      Serial.write(OKAY_CHARACTER);

      if(command == handshake_command) {
        Serial.write(ARDUINO_NUMBER);
      }
      if(command == move_command) {
        move(parameter);
        Serial.write(DONE_CHARACTER);
      }
      else if(command == pick_command) {
        pick();
        Serial.write(DONE_CHARACTER);
      }
      else if(command == place_command) {
        place();
        Serial.write(DONE_CHARACTER);
      }
    }

    else {
      Serial.write(NOT_OKAY_CHARACTER);
      //flush buffer
      while(Serial.available() > 0) {
        Serial.read();
      }
    }
  }
}

void pick() {
  gripper_servo.write(gripper_servo_release_angle);
  delay(DELAY);
  vertical_servo.write(vertical_servo_down_angle);
  delay(DELAY);
  gripper_servo.write(gripper_servo_grab_angle);
  delay(DELAY);
  vertical_servo.write(vertical_servo_up_angle);
  delay(DELAY);
}

void place() {
  vertical_servo.write(vertical_servo_down_angle);
  delay(DELAY);
  gripper_servo.write(gripper_servo_release_angle);
  delay(DELAY);
  vertical_servo.write(vertical_servo_up_angle);
  delay(DELAY); 
}

void move(int position) {
  rotation_servo.write(position);
  delay(10);
}

void _blink_() {
  digitalWrite(13,HIGH);
  delay(500);
  digitalWrite(13,LOW);
  delay(500);
}
