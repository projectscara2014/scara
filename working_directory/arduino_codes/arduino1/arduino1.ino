//NOTE: All flags are binary ( 0 or 1)

//FLAGS -- Mainloop
int flag_ldr;
int flag_check_5v_brownout = 1;
int flag_check_12v_brownout = 0;

// FLAGS -- Status
int flag_5v_brownout_detected = 0;
int flag_12v_brownout_detected = 0;

//THRESHOLDS
int threshold_12v = 512; //#CHANGE
int threshold_5v = 512; //#CHANGE

//Pin Definitions
char pin_5v_brownout = A3;
char pin_12v_brownout = A4;
char pin_ldr_1 = A1;
char pin_ldr_2 = A2;

//Other Definitions
int input_5v;
int input_12v;
char serial_command;

void setup() {
	Serial.begin(57600);

	//Pin Initializations
	pinMode(pin_5v_brownout,INPUT);
	pinMode(pin_12v_brownout,INPUT);
	pinMode(pin_ldr_1,INPUT);
	pinMode(pin_ldr_2,INPUT);

	// Safety Initializations
	turn_off_dynamixel();

}

void loop() {
	// checks for serial communication
	if(Serial.available()>0){
		serial_command = Serial.read();
		service_serial_command(serial_command);
	}

	// checks for 12 Volt brown out
	if(flag_check_12v_brownout == 1){
		check_for_12v_brownout();
	}

	// checks for 5 Volt brown out
	if(flag_check_5v_brownout == 1){
		check_for_12v_brownout();
	}
}

void service_serial_command(char serial_command){
	// This function is used for calling various functions as per the serial command. 
	
	//#CHANGE
}

void check_for_12v_brownout(){
	input_12v = analogRead(pin_12v_brownout);
	// CHANGE LATER (to ensure actual brownout and not a minor fluctuation)
	if(input_12v<threshold_12v){
		turn_off_dynamixel();
		flag_12v_brownout_detected = 1;
		flag_check_12v_brownout = 0;
	}
}

void check_for_5v_brownout(){
	input_5v = analogRead(pin_5v_brownout);
	if(flag_5v_brownout_detected == 1){
		// CHANGE LATER (to ensure actual brownout and not a minor fluctuation)
		if(input_5v<threshold_5v){
			turn_on_backup_battery();
			flag_5v_brownout_detected = 1;
		}
	}
	else{
		if(input_5v>threshold_5v){
			turn_off_backup_battery();
			flag_5v_brownout_detected = 0;
		}
	}
	
}

void turn_off_dynamixel(){
	// This function will turn off the dynamixel

	//#CHANGE
}

void turn_on_backup_battery(){
	// This function will turn on backup battery

	//#CHANGE
}

void turn_off_backup_battery(){
	// This function will turn off backup battery

	//#CHANGE
}
