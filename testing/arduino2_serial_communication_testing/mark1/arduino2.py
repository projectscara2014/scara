import serial
import time
from debug import debug

def init(arduino_serial_object) : 
	global arduino
	arduino = arduino_serial_object

# --------------- TESTING ------------------
arduino = serial.Serial('/dev/tty.usbmodem1421')
arduino.baudrate = 57600

# ------------ PYTHON BYTES ----------------
START_BYTE_1 = 255
START_BYTE_2 = 254
#-------------------------------------------

# ------------ PYTHON COMMANDS -------------
GET_OUT_OF_RESET_COMMAND = 1
HANDSHAKE_COMMAND = 2
PICK_COMMAND = 3
PLACE_COMMAND = 4
MOVE_COMMAND = 5
# ------------------------------------------

# ----------- COMMAND DONE TIMES -----------
GET_OUT_OF_RESET_COMMAND_OF_RESET_COMMAND_DONE_TIME = 2
PICK_COMMAND_DONE_TIME = 13
PLACE_COMMAND_DONE_TIME = 10
MOVE_COMMAND_DONE_TIME = 5
# ------------------------------------------

# -------- ARDUINO RETURN CHARACTERS -------
IN_RESET_CHARACTER = 1
ARDUINO_NUMBER_CHARACTER = 2
OKAY_CHARACTER = 3
NOT_OKAY_CHARACTER = 4
DONE_CHARACTER = 5
INVALID_COMMAND_CHARACTER = 6
# ------------------------------------------

# ---------------- VARIABLES ---------------
GO_TO_SERVO_POS = 0
OKAY_TIME_THRESHOLD = 2
SEND_INSTRUCTION_COUNT_THRESHOLD = 5
# ------------------------------------------

@debug()
def write(instruction,parameter) :
	print(get_instruction_name(instruction)) 
	arduino.write(chr(START_BYTE_1))
	arduino.write(chr(START_BYTE_2)) 
	arduino.write(chr(instruction)) 
	arduino.write(chr(parameter)) 

def get_instruction_name(instruction) : 
	if instruction == GET_OUT_OF_RESET_COMMAND : 
		return 'GET_OUT_OF_RESET_COMMAND'
	elif instruction == PICK_COMMAND : 
		return 'PICK_COMMAND'
	elif instruction == PLACE_COMMAND : 
		return 'PLACE_COMMAND'
	elif instruction == MOVE_COMMAND : 
		return 'MOVE_COMMAND'
	else : 
		return 0

# -handling if IN_RESET_CNARACTER received-

@debug()
def get_done_time(instruction) : 
	if instruction == GET_OUT_OF_RESET_COMMAND : 
		return GET_OUT_OF_RESET_COMMAND_DONE_TIME
	elif instruction == PICK_COMMAND : 
		return PICK_COMMAND_DONE_TIME
	elif instruction == PLACE_COMMAND : 
		return PLACE_COMMAND_DONE_TIME
	elif instruction == MOVE_COMMAND : 
		return MOVE_COMMAND_DONE_TIME
	else : 
		return 0

@debug()
def send_and_wait(send_and_wait_count_threshold,instruction,parameter) : 
	send_and_wait_count = 0
	while send_and_wait_count < send_and_wait_count_threshold : 
		write(instruction,parameter)
		elapsed_time = 0
		start_time = time.time()

		while (elapsed_time <= OKAY_TIME_THRESHOLD) and (arduino.inWaiting() == 0) : 
			elapsed_time = time.time() - start_time
		print('send_and_wait - done_character - elapsed time - {0}'.format(elapsed_time))

		if(elapsed_time > OKAY_TIME_THRESHOLD) : 
			# did not receive any response
			send_and_wait_count += 1
			# write(instruction,parameter)
		else :
			return_character = ord(arduino.read(1))
			if(return_character != OKAY_CHARACTER) : 
				# received something other that okay character
				print('received something other that okay character - {0}'.format(return_character))
				send_and_wait_count += 1
				# write(instruction,parameter)
			else : 
				# received okay character
				elapsed_time = 0
				start_time = time.time()
				done_time_threshold = get_done_time(instruction)

				while (elapsed_time <= done_time_threshold) and (arduino.inWaiting() == 0) : 
					elapsed_time = time.time() - start_time
				print('send_and_wait - done_character - elapsed time - {0}'.format(elapsed_time))
				if(elapsed_time > done_time_threshold) : 
					# did not receive ant character
					send_and_wait_count += 1
					# write(instruction,parameter)
				elif(ord(arduino.read(1)) != DONE_CHARACTER) : 
					# received something other than done character
					send_and_wait_count += 1
					# write(instruction,parameter)
				else : 
					# received done character
					return True
		return False

@debug()
def reset_send_and_wait() : 
	if not send_and_wait(5,GET_OUT_OF_RESET_COMMAND,0) : 
		print('could not unreset arduino')
		return False
	print('arduino has been unreset')
	return send_and_wait(5,MOVE_COMMAND,GO_TO_SERVO_POS)
#-----------------------------------------

@debug()
def send_and_check(instruction,parameter=0) : 
	arduino.read(arduino.inWaiting())
	send_instruction_count = 0

	while(send_instruction_count < SEND_INSTRUCTION_COUNT_THRESHOLD) : 
		write(instruction,parameter)
		elapsed_time = 0
		start_time = time.time()
		while (elapsed_time <= OKAY_TIME_THRESHOLD) and (arduino.inWaiting() == 0) : 
			elapsed_time = time.time() - start_time
		print('send_and_check - okay_character - elapsed time - {0}'.format(elapsed_time))
		if(elapsed_time > OKAY_TIME_THRESHOLD) : 
			send_instruction_count += 1
			# write(instruction,parameter)
		else : 
			return_character = ord(arduino.read(1)) 

			# NOT_OKAY_CHARACTER
			if(return_character == NOT_OKAY_CHARACTER) : 
				send_instruction_count += 1
				# write(instruction,parameter)
			
			# ARDUINO NUMBER CHARACTER
			elif(return_character == ARDUINO_NUMBER_CHARACTER) : 
				if(instruction == HANDSHAKE_COMMAND) : 
					return True
				else : 
					send_instruction_count += 1
					# write(instruction,parameter)

			# IN RESET CHARACTER
			elif(return_character == IN_RESET_CHARACTER) : 
				print('arduino has been reset')
				if not reset_send_and_wait() : 
					raise OSError # EXCEPTION HANDLING
				send_instruction_count += 1
				# write(instruction,parameter)
			
			# INVALID INSTRUCTION CHARACTER
			elif(return_character == INVALID_COMMAND_CHARACTER) : 
				raise OSError('Something is wrong, arduino received invalid instrucction')

			# OKAY CHARACTER
			elif(return_character == OKAY_CHARACTER) : 
				elapsed_time = 0
				start_time = time.time()
				done_time_threshold = get_done_time(instruction)

				while (elapsed_time <= done_time_threshold) and (arduino.inWaiting() == 0) : 
					elapsed_time = time.time() - start_time
				print('send_and_check - done_character - elapsed time - {0}'.format(elapsed_time))
				if(elapsed_time > done_time_threshold) : 
					send_instruction_count += 1
					# write(instruction,parameter)
				elif(ord(arduino.read(1)) != DONE_CHARACTER) : 
					send_instruction_count += 1
					# write(instruction,parameter)
				else : 
					return True

			else : 
				raise OSError('Something is worng, arduino sent wrong return character - {0}'.format(return_character))
	return False

@debug()
def handshake() : 
	send_and_check(HANDSHAKE_COMMAND)

@debug()
def pick() : 
	send_and_check(PICK_COMMAND)

@debug()
def place() : 
	send_and_check(PLACE_COMMAND)

@debug()
def move(position) : 
	send_and_check(MOVE_COMMAND)
