import serial
import time

def init(arduino_serial_object):
	global arduino
	arduino = arduino_serial_object

GO_TO_SERVO_POS = 0

START_BYTE = 255			#'\xff'
PICK_COMMAND = 97			# "a"
PLACE_COMMAND = 98			# "b"
MOVE_COMMAND = 99			# "c"
OKAY_CHARACTER = 'O'		# Okay I am doing it
DONE_CHARACTER = 'D'		# DONE
NOT_OKAY_CHARACTER = 'N'	# Not Okay

ROTATE_COMMUNICATION_TIMEOUT_LIMIT = 10
PICK_COMMUNICATION_TIMEOUT_LIMIT = 25
PLACE_COMMUNICATION_TIMEOUT_LIMIT = 25

def send_and_check(instruction_packet,timeout=5) :
	# print(timeout) 
	global arduino

	arduino.write(instruction_packet) 
	start_time = time.time()
	elapsed_time = 0
	FLAG = 0
	while elapsed_time < timeout and FLAG != 2:
		elapsed_time = time.time() - start_time
		if arduino.inWaiting() > 0 :
			returned_data = arduino.read(arduino.inWaiting())
			# print(returned_data)
			if OKAY_CHARACTER in returned_data :
				FLAG += 1
			if DONE_CHARACTER in returned_data :
				FLAG += 1 
			if NOT_OKAY_CHARACTER in returned_data : 
				arduino.write(instruction_packet)
	if FLAG != 2 : 
		raise OSError('arduino not responding')
		# EXCEPTION HANDLING

def rotate() :
	global GO_TO_SERVO_POS 
	GO_TO_SERVO_POS = int(GO_TO_SERVO_POS)
	print(START_BYTE)
	print(MOVE_COMMAND)
	print(GO_TO_SERVO_POS)
	instruction_packet = chr(START_BYTE) + chr(MOVE_COMMAND) + chr(GO_TO_SERVO_POS)
	send_and_check(instruction_packet,timeout = ROTATE_COMMUNICATION_TIMEOUT_LIMIT)

def pick() :
	instruction_packet = chr(START_BYTE) + chr(PICK_COMMAND) + chr(0)
	send_and_check(instruction_packet,timeout = PICK_COMMUNICATION_TIMEOUT_LIMIT)

def place() : 
	instruction_packet = chr(START_BYTE) + chr(PLACE_COMMAND) + chr(0)
	send_and_check(instruction_packet,timeout = PLACE_COMMUNICATION_TIMEOUT_LIMIT)

# instruction_packet = chr(START_BYTE) + 'h' + chr(0)
# send_and_check(instruction_packet)
# print(arduino.read(arduino.inWaiting()))
