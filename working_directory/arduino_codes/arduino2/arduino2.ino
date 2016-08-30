// -------------- IRONSTEIN0
#include<Servo.h>

//------ SERVO CALIBRATED POSITIONS --------- 
float gripper_servo_grab_angle=20;
float gripper_servo_release_angle=100;
int vertical_servo_down_angle = 80;
int vertical_servo_up_angle = 140;

int gripper_servo_initial_position = 90;
int vertical_servo_initial_position = 120;
int rotation_servo_initial_position = 90;
// ------------------------------------------

// ---------- SERVO PIN ATTACHMENTS ---------
Servo rotation_servo;
Servo vertical_servo;
Servo gripper_servo;

int vertical_servo_pin = 6;
int rotation_servo_pin = 5;
int gripper_servo_pin =  3;
// ------------------------------------------

// --------- REGISTER DECLARATIONS ----------
int state_reg;
int hand_state_reg;
// ------------------------------------------

// ----------- STATE DECLARATIONS -----------
int STATE_RESET = 0;
int STATE_NOT_RESET = 1;
int HAND_STATE_PICK = 0;
int HAND_STATE_PLACE = 1;
int HAND_STATE_RESET = 2;
// ------------------------------------------

// ------------- PYTHON BYTES ---------------
int START_BYTE_1 = 255;
int START_BYTE_2 = 254;
// ------------------------------------------

// ---------- PYTHON COMMANDS ---------------
int GET_OUT_OF_RESET_COMMAND = 1;
int HANDSHAKE_COMMAND = 2;
int PICK_COMMAND = 3;
int PLACE_COMMAND = 4;
int MOVE_COMMAND = 5;
int GO_TO_RESET_COMMAND = 6;
// ------------------------------------------

// ------- ARDUINO RETURN CHARACTERS --------
int IN_RESET_CHARACTER = 1          + 48;
int ARDUINO_NUMBER_CHARACTER = 2    + 48;
int OKAY_CHARACTER = 3              + 48;
int NOT_OKAY_CHARACTER = 4          + 48;
int DONE_CHARACTER = 5              + 48;
int INVALID_COMMAND_CHARACTER = 6   + 48;
// ------------------------------------------

// --------------- VARIABLES ----------------
int DELAY = 3000;
int val_0_rot = 1248;
int val_90_rot = 2172;
// ------------------------------------------

void setup() {
	
	// serial communication setup
	Serial.begin(57600);

        // Pin 13 LED
	pinMode(13,OUTPUT);
	digitalWrite(13,LOW);

	// servo connection setup
	// rotation_servo.attach(rotation_servo_pin);
	pinMode(rotation_servo_pin,OUTPUT);
	digitalWrite(rotation_servo_pin,LOW);
  	vertical_servo.attach(vertical_servo_pin);
  	gripper_servo.attach(gripper_servo_pin);
	
        // reset
        reset();

}

void loop() {

	if(Serial.available() == 4) {
		int start_byte_1 = Serial.read();
		int start_byte_2 = Serial.read();
		int command = Serial.read();
		int parameter = Serial.read();

		if((start_byte_1 == START_BYTE_1)&&(start_byte_2 == START_BYTE_2)) {
			// valid instruction packet
			if(command == HANDSHAKE_COMMAND) {
				// return arduino number
				Serial.write(char(ARDUINO_NUMBER_CHARACTER));
			} else {

				if(state_reg == STATE_RESET) {
					// in reset
					if(command == GET_OUT_OF_RESET_COMMAND) {
						// get out of reset
						state_reg = STATE_NOT_RESET;
						Serial.write(char(OKAY_CHARACTER));
            			Serial.write(char(DONE_CHARACTER));

					} else {
						Serial.write(IN_RESET_CHARACTER);
					}

				} else {
					// not in reset
					if(command == PICK_COMMAND) {
						Serial.write(char(OKAY_CHARACTER));
						pick();
						Serial.write(char(DONE_CHARACTER));
					} else if(command == PLACE_COMMAND) {
						Serial.write(char(OKAY_CHARACTER));
						place();
						Serial.write(char(DONE_CHARACTER));
					} else if(command == MOVE_COMMAND) {
						Serial.write(char(OKAY_CHARACTER));
						move(parameter);
						Serial.write(char(DONE_CHARACTER));
					} else if(command == GO_TO_RESET_COMMAND) {
                                                Serial.write(char(OKAY_CHARACTER));
                                                reset();
                                                Serial.write(char(DONE_CHARACTER));
                                        } else {
            Serial.write(char(INVALID_COMMAND_CHARACTER));
					}
				}
			}

		} else {
			// invalid instruction packet
			delay(1000); // wait for all bytes to be received
			Serial.write(char(NOT_OKAY_CHARACTER));
			// flush buffer
			while(Serial.available()) {
				Serial.read();
			}
		}
	}

	if(state_reg == STATE_RESET) {
		digitalWrite(13,HIGH);
	} else {
		digitalWrite(13,LOW);
	}
}

void pick() {
	// Serial.write("picking up");
	if(hand_state_reg == HAND_STATE_PICK) {
		delay(10);
	} else {
		gripper_servo.write(gripper_servo_release_angle);
		delay(DELAY);
		vertical_servo.write(vertical_servo_down_angle);
		delay(DELAY);
		gripper_servo.write(gripper_servo_grab_angle);
		delay(DELAY);
		vertical_servo.write(vertical_servo_up_angle);
		delay(DELAY);
		// double_blink();
		hand_state_reg = HAND_STATE_PICK;
	}
}

void place() {
	// Serial.write("placing");
	if(hand_state_reg == HAND_STATE_PLACE) {
		delay(10);
	} else {
		vertical_servo.write(vertical_servo_down_angle);
		delay(DELAY);
		gripper_servo.write(gripper_servo_release_angle);
		delay(DELAY);
		vertical_servo.write(vertical_servo_up_angle);
		delay(DELAY); 
		// double_blink();
		hand_state_reg = HAND_STATE_PLACE;
	}
}

// void move(int angle) {
// 	rotation_servo.write(angle);
// 	delay(DELAY);
//   double_blink();
// }

void move(int angle){
//	rotation_servo.write(angle);
	int angle_ = angle%90;
        if(angle_ == 0) {
          blink();
        } else if(angle_ == 90) {
          double_blink();
        } else if(angle_ == 180) {
          triple_blink();
        }
	float f;
	f = ((val_90_rot-val_0_rot)*1.0*angle_/90) + val_0_rot;
	angle_ = int(f);
	_move_3_(angle_);
}

void _move_3_(int on_time){
	int off_time = 20000 - on_time;
	for(int i = 0;i<25;i++){
		digitalWrite(rotation_servo_pin,HIGH);
		delay(on_time/1000);
		delayMicroseconds(on_time%1000);
		digitalWrite(rotation_servo_pin,LOW);
		delay(off_time/1000);
		delayMicroseconds(off_time%1000);
	}
}

void blink() {
  digitalWrite(13,HIGH);
  delay(100);
  digitalWrite(13,LOW);
  delay(100);
}

void double_blink() {
  blink();
  blink();
}

void triple_blink() {
	double_blink();
	blink();
}

void reset() {
  rotation_servo.write(rotation_servo_initial_position);
  vertical_servo.write(vertical_servo_initial_position);
  gripper_servo.write(gripper_servo_initial_position);
	
  // state setup
  state_reg = STATE_RESET;
  hand_state_reg = HAND_STATE_RESET;
}
