import serial
import time
# from utils.debug import debug

arduino = None

def init(arduino_serial_object) : 
	global arduino
	arduino = arduino_serial_object
	reset()

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
GO_TO_RESET_COMMAND = 6
# ------------------------------------------

# ----------- COMMAND DONE TIMES -----------
GET_OUT_OF_RESET_COMMAND_DONE_TIME = 2
PICK_COMMAND_DONE_TIME = 13
PLACE_COMMAND_DONE_TIME = 10
MOVE_COMMAND_DONE_TIME = 5
GO_TO_RESET_COMMAND_DONE_TIME = 2
HANDSHAKE_COMMAND_DONE_TIME = 2
# ------------------------------------------

# -------- ARDUINO RETURN CHARACTERS -------
IN_RESET_CHARACTER = 1				+ 48
ARDUINO_NUMBER_CHARACTER = 2		+ 48
OKAY_CHARACTER = 3					+ 48
NOT_OKAY_CHARACTER = 4				+ 48
DONE_CHARACTER = 5					+ 48
INVALID_COMMAND_CHARACTER = 6		+ 48
# ------------------------------------------

# ---------------- VARIABLES ---------------
GO_TO_SERVO_POS = 0
OKAY_TIME_THRESHOLD = 2
SEND_INSTRUCTION_COUNT_THRESHOLD = 5
# ------------------------------------------

# @debug()
def write(instruction,parameter) :
	print("Arduino2 Command => " + get_instruction_name(instruction)) 
	arduino.write(chr(START_BYTE_1))
	time.sleep(0.1)
	arduino.write(chr(START_BYTE_2)) 
	time.sleep(0.1)
	arduino.write(chr(instruction)) 
	time.sleep(0.1)
	arduino.write(chr(parameter)) 
	time.sleep(0.1)

def get_instruction_name(instruction) : 
	if instruction == GET_OUT_OF_RESET_COMMAND : 
		return 'GET_OUT_OF_RESET_COMMAND'
	elif instruction == PICK_COMMAND : 
		return 'PICK_COMMAND'
	elif instruction == PLACE_COMMAND : 
		return 'PLACE_COMMAND'
	elif instruction == MOVE_COMMAND : 
		return 'MOVE_COMMAND'
	elif instruction == HANDSHAKE_COMMAND :
		return 'HANDSHAKE_COMMAND'
	elif instruction == GO_TO_RESET_COMMAND:
		return 'GO_TO_RESET_COMMAND'
	else : 
		print("arduino2 - get_instruction_name - invalid instruction")
		import sys
		sys.exit(1)

# -handling if IN_RESET_CNARACTER received-

# @debug()
def get_done_time(instruction) : 
	if instruction == GET_OUT_OF_RESET_COMMAND : 
		return GET_OUT_OF_RESET_COMMAND_DONE_TIME
	elif instruction == PICK_COMMAND : 
		return PICK_COMMAND_DONE_TIME
	elif instruction == PLACE_COMMAND : 
		return PLACE_COMMAND_DONE_TIME
	elif instruction == MOVE_COMMAND : 
		return MOVE_COMMAND_DONE_TIME
	elif instruction == GO_TO_RESET_COMMAND : 
		return GO_TO_RESET_COMMAND_DONE_TIME
	elif instruction == HANDSHAKE_COMMAND : 
		return HANDSHAKE_COMMAND_DONE_TIME
	else : 
		return 0

# @debug()
def send_and_wait(send_and_wait_count_threshold,instruction,parameter) : 
	send_and_wait_count = 0
	while send_and_wait_count < send_and_wait_count_threshold : 
		write(instruction,parameter)
		elapsed_time = 0
		start_time = time.time()

		while (elapsed_time <= OKAY_TIME_THRESHOLD) and (arduino.inWaiting() == 0) : 
			elapsed_time = time.time() - start_time
		print('send_and_wait - okay_character - elapsed time - {0}'.format(elapsed_time))

		if(elapsed_time > OKAY_TIME_THRESHOLD) : 
			# did not receive any response
			send_and_wait_count += 1
			# write(instruction,parameter)
		else :
			return_character = ord(arduino.read(1))
			print('-------1-------')
			print(return_character)
			print('--------------')

			if(return_character == OKAY_CHARACTER) :
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
					if(arduino.inWaiting() != 0) and (arduino.read(1) == IN_RESET_CHARACTER) :
						write(GET_OUT_OF_RESET_COMMAND,0)
						time.sleep(2)
						arduino.read(arduino.inWaiting())
						send_and_wait_count += 1
				else : 
					return_character = ord(arduino.read(1))
					print('--------2------')
					print(return_character)
					print('--------------')
					if(return_character == IN_RESET_CHARACTER) : 
						# received in reset character
						write(GET_OUT_OF_RESET_COMMAND,0)
						time.sleep(2)
						arduino.read(arduino.inWaiting())
						send_and_wait_count += 1

					elif(return_character == DONE_CHARACTER) : 
						return True
					else :
						# received something other than done character
						send_and_wait_count += 1
						# write(instruction,parameter)

			elif(return_character == IN_RESET_CHARACTER) : 
				# received in reset character
				write(GET_OUT_OF_RESET_COMMAND,0)
				time.sleep(2)
				arduino.read(arduino.inWaiting()) 
				send_and_wait_count += 1
				
			else : 
				# received something other that okay character
				print('received something other that okay character - {0}'.format(return_character))
				send_and_wait_count += 1
				# write(instruction,parameter)

	return False

# @debug()
def reset_send_and_wait() : 
	if not send_and_wait(5,GET_OUT_OF_RESET_COMMAND,0) : 
		print('could not unreset arduino')
		return False
	print('arduino has been unreset')
	return send_and_wait(5,MOVE_COMMAND,GO_TO_SERVO_POS)
#-----------------------------------------

# @debug()
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
				# raise OSError('Something is worng, arduino sent wrong return character - {0}'.format(return_character))
				send_instruction_count += 1
				# return False
	return False

# @debug()
def handshake() : 
	return send_and_check(HANDSHAKE_COMMAND)

# @debug()
def pick() : 
	send_and_check(PICK_COMMAND)

# @debug()
def place() : 
	send_and_check(PLACE_COMMAND)

# @debug()
def rotate() : 
	send_and_check(MOVE_COMMAND,int(GO_TO_SERVO_POS))

def reset():
	send_and_check(GO_TO_RESET_COMMAND)



# # --------------- TESTING ------------------

# arduino = serial.Serial('com6')
# arduino.baudrate = 57600
# handshake()
# time.sleep(7)
# pick()
# time.sleep(5)
# pick()
# time.sleep(5)
# reset()
# # time.sleep(5)
# # handshake()
# time.sleep(5)
# pick()



# # pick()
# # time.sleep(5)
# # GO_TO_SERVO_POS = 45
# # rotate()
# # GO_TO_SERVO_POS = 135
# # time.sleep(3)
# # rotate()
# # time.sleep(3)
# # place()
# # for i in range(10) : 
# # 	print(i)
# 	# GO_TO_SERVO_POS = 89
# 	# rotate()
# 	# time.sleep(5)
# 	# place()
# 	# time.sleep(5)
# 	# GO_TO_SERVO_POS = 20
# 	# rotate()
# 	# time.sleep(5)
# 	# pick()
# 	# time.sleep(5)
# # place()
# # pick()

# for i in range(50):
# 	place()
# 	pick()








### -------- Commented on 12/7/16 ( Not sure if its working ) ----- ###
# import serial
# import time

# def init(arduino_serial_object):
# 	global arduino
# 	arduino = arduino_serial_object

# GO_TO_SERVO_POS = 0

# START_BYTE = 255					#'\xff'
# PICK_COMMAND = 97					# "a"
# PLACE_COMMAND = 98					# "b"
# MOVE_COMMAND = 99					# "c"
# MOVE_OUT_OF_RESET_COMMAND = 114 	# "r"
# OKAY_CHARACTER = 'O'				# Okay I am doing it
# DONE_CHARACTER = 'D'				# DONE
# NOT_OKAY_CHARACTER = 'N'			# Not Okay
# IN_RESET_CHARACTER = 'R'			# Arduino Has been reset

# ROTATE_COMMUNICATION_TIMEOUT_LIMIT = 2
# PICK_COMMUNICATION_TIMEOUT_LIMIT = 12
# PLACE_COMMUNICATION_TIMEOUT_LIMIT = 12

# SEND_AND_CHECK_RECURSION_DEPTH = 0
# SEND_AND_CHECK_RECURSION_DEPTH_LIMIT = 5

# NUMBER_OF_TIMES_SENT = 0
# NUMBER_OF_TIMES_SENT_LIMIT = 100

# def send_and_check(instruction_packet,timeout=5) :
# 	global SEND_AND_CHECK_RECURSION_DEPTH 
# 	global NUMBER_OF_TIMES_SENT

# 	# print('sending')

# 	# print(timeout) 

# 	NUMBER_OF_TIMES_SENT += 1
# 	# print('number of times sent --> ',NUMBER_OF_TIMES_SENT)

# 	arduino.write(instruction_packet) 
# 	time.sleep(0.5)
# 	start_time = time.time()
# 	elapsed_time = 0
# 	FLAG = 0
# 	while elapsed_time < timeout and FLAG != 2:
# 		elapsed_time = time.time() - start_time	
# 		if arduino.inWaiting() > 0 :
# 			returned_data = arduino.read(arduino.inWaiting())
# 			# print(returned_data)
# 			if IN_RESET_CHARACTER in returned_data :
# 				print('arduino2 has been reset')
# 				send_and_check(chr(START_BYTE) + chr(MOVE_OUT_OF_RESET_COMMAND) + chr(0))	# is timeout - elapsed_time correct
# 				print('moving servo hand to previous position')
# 				rotate()

# 			if OKAY_CHARACTER in returned_data :
# 				FLAG += 1
# 			if DONE_CHARACTER in returned_data :
# 				FLAG += 1 
# 			if NOT_OKAY_CHARACTER in returned_data : 
# 				arduino.write(instruction_packet)
# 	if FLAG != 2 : 
# 		if NUMBER_OF_TIMES_SENT == NUMBER_OF_TIMES_SENT_LIMIT + 1:
# 			raise OSError('arduino2 not responding')
# 			# EXCEPTION HANDLING
# 		else :
# 			NUMBER_OF_TIMES_SENT += 1
# 			send_and_check(instruction_packet, timeout = timeout)

# def reset_communication_flags() :
# 	global NUMBER_OF_TIMES_SENT,SEND_AND_CHECK_RECURSION_DEPTH
# 	NUMBER_OF_TIMES_SENT = 0
# 	SEND_AND_CHECK_RECURSION_DEPTH = 0

# def rotate() :
# 	global GO_TO_SERVO_POS 
# 	GO_TO_SERVO_POS = int(GO_TO_SERVO_POS)
# 	print(START_BYTE)
# 	print(MOVE_COMMAND)
# 	print(GO_TO_SERVO_POS)
# 	instruction_packet = chr(START_BYTE) + chr(MOVE_COMMAND) + chr(GO_TO_SERVO_POS)
# 	send_and_check(instruction_packet,timeout = ROTATE_COMMUNICATION_TIMEOUT_LIMIT)
# 	reset_communication_flags()

# def pick() :
# 	instruction_packet = chr(START_BYTE) + chr(PICK_COMMAND) + chr(0)
# 	send_and_check(instruction_packet,timeout = PICK_COMMUNICATION_TIMEOUT_LIMIT)
# 	reset_communication_flags()

# def place() : 
# 	instruction_packet = chr(START_BYTE) + chr(PLACE_COMMAND) + chr(0)
# 	send_and_check(instruction_packet,timeout = PLACE_COMMUNICATION_TIMEOUT_LIMIT)
# 	reset_communication_flags()

# # instruction_packet = chr(START_BYTE) + 'h' + chr(0)
# # send_and_check(instruction_packet)
# # print(arduino.read(arduino.inWaiting()))
