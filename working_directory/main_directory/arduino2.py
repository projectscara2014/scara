import serial
import time

def init(arduino_serial_object):
	global arduino
	arduino = arduino_serial_object

GO_TO_SERVO_POS = 0

START_BYTE = 255					#'\xff'
PICK_COMMAND = 97					# "a"
PLACE_COMMAND = 98					# "b"
MOVE_COMMAND = 99					# "c"
MOVE_OUT_OF_RESET_COMMAND = 114 	# "r"
OKAY_CHARACTER = 'O'				# Okay I am doing it
DONE_CHARACTER = 'D'				# DONE
NOT_OKAY_CHARACTER = 'N'			# Not Okay
IN_RESET_CHARACTER = 'R'			# Arduino Has been reset

ROTATE_COMMUNICATION_TIMEOUT_LIMIT = 2
PICK_COMMUNICATION_TIMEOUT_LIMIT = 12
PLACE_COMMUNICATION_TIMEOUT_LIMIT = 12

SEND_AND_CHECK_RECURSION_DEPTH = 0
SEND_AND_CHECK_RECURSION_DEPTH_LIMIT = 5

NUMBER_OF_TIMES_SENT = 0
NUMBER_OF_TIMES_SENT_LIMIT = 100

def send_and_check(instruction_packet,timeout=5) :
	global SEND_AND_CHECK_RECURSION_DEPTH 
	global NUMBER_OF_TIMES_SENT

	# print('sending')

	# print(timeout) 

	NUMBER_OF_TIMES_SENT += 1
	# print('number of times sent --> ',NUMBER_OF_TIMES_SENT)

	arduino.write(instruction_packet) 
	time.sleep(0.5)
	start_time = time.time()
	elapsed_time = 0
	FLAG = 0
	while elapsed_time < timeout and FLAG != 2:
		elapsed_time = time.time() - start_time	
		if arduino.inWaiting() > 0 :
			returned_data = arduino.read(arduino.inWaiting())
			# print(returned_data)
			if IN_RESET_CHARACTER in returned_data :
				print('arduino2 has been reset')
				send_and_check(chr(START_BYTE) + chr(MOVE_OUT_OF_RESET_COMMAND) + chr(0))	# is timeout - elapsed_time correct
				print('moving servo hand to previous position')
				rotate()

			if OKAY_CHARACTER in returned_data :
				FLAG += 1
			if DONE_CHARACTER in returned_data :
				FLAG += 1 
			if NOT_OKAY_CHARACTER in returned_data : 
				arduino.write(instruction_packet)
	if FLAG != 2 : 
		if NUMBER_OF_TIMES_SENT == NUMBER_OF_TIMES_SENT_LIMIT + 1:
			raise OSError('arduino2 not responding')
			# EXCEPTION HANDLING
		else :
			NUMBER_OF_TIMES_SENT += 1
			send_and_check(instruction_packet, timeout = timeout)

def reset_communication_flags() :
	global NUMBER_OF_TIMES_SENT,SEND_AND_CHECK_RECURSION_DEPTH
	NUMBER_OF_TIMES_SENT = 0
	SEND_AND_CHECK_RECURSION_DEPTH = 0

def rotate() :
	global GO_TO_SERVO_POS 
	GO_TO_SERVO_POS = int(GO_TO_SERVO_POS)
	print(START_BYTE)
	print(MOVE_COMMAND)
	print(GO_TO_SERVO_POS)
	instruction_packet = chr(START_BYTE) + chr(MOVE_COMMAND) + chr(GO_TO_SERVO_POS)
	send_and_check(instruction_packet,timeout = ROTATE_COMMUNICATION_TIMEOUT_LIMIT)
	reset_communication_flags()

def pick() :
	instruction_packet = chr(START_BYTE) + chr(PICK_COMMAND) + chr(0)
	send_and_check(instruction_packet,timeout = PICK_COMMUNICATION_TIMEOUT_LIMIT)
	reset_communication_flags()

def place() : 
	instruction_packet = chr(START_BYTE) + chr(PLACE_COMMAND) + chr(0)
	send_and_check(instruction_packet,timeout = PLACE_COMMUNICATION_TIMEOUT_LIMIT)
	reset_communication_flags()

# instruction_packet = chr(START_BYTE) + 'h' + chr(0)
# send_and_check(instruction_packet)
# print(arduino.read(arduino.inWaiting()))
