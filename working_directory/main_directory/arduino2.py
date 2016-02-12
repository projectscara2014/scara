import serial
import time

#--------------------- ARDUINO SETUP --------------------------
arduino = serial.Serial('/dev/cu.usbmodem1421')
# from subordinate_directory import serial_ports_setup
# arduino = serial_ports_setup.find_dynamixel_and_arduino()
def decorate_serial_object(serial_object) : 
	
	def decorator(function) :
		def wrapper(*args,**kwargs) : 
			return_value = None
			try : 
				return_value = function(*args,**kwargs)
			except OSError :
				print('arduino not connected')
			else :
				return return_value
		return wrapper

	def set_baudrate(baudrate) : 
		try :
			serial_object.baudrate = baudrate
		except serial.serialutil.SerialException :
			print('arduino not connected')
	
	serial_object.write = decorator(serial_object.write)
	serial_object.read = decorator(serial_object.read)
	serial_object.inWaiting = decorator(serial_object.inWaiting)
	serial_object.set_baudrate = set_baudrate
	return serial_object
#--------------------------------------------------------------

arduino = decorate_serial_object(arduino)
arduino.set_baudrate(57600)

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
	print(timeout) 
	arduino.write(instruction_packet) 
	start_time = time.time()
	elapsed_time = 0
	FLAG = 0
	while elapsed_time < timeout and FLAG != 2:
		elapsed_time = time.time() - start_time
		if arduino.inWaiting() > 0 :
			returned_data = arduino.read(arduino.inWaiting())
			if OKAY_CHARACTER in returned_data :
				FLAG += 1
			elif DONE_CHARACTER in returned_data :
				FLAG += 1 
			elif NOT_OKAY_CHARACTER in returned_data : 
				arduino.write(instruction_packet)
	if FLAG != 2 : 
		raise OSError('arduino not responding')
		# EXCEPTION HANDLING

def rotate() :
	global GO_TO_SERVO_POS 
	instruction_packet = chr(START_BYTE) + chr(MOVE_COMMAND) + chr(GO_TO_SERVO_POS)
	send_and_check(instruction_packet,timeout = ROTATE_COMMUNICATION_TIMEOUT_LIMIT)

def pick() :
	instruction_packet = chr(START_BYTE) + chr(PICK_COMMAND) + chr(0)
	send_and_check(instruction_packet,timeout = PICK_COMMUNICATION_TIMEOUT_LIMIT)

def place() : 
	instruction_packet = chr(START_BYTE) + chr(PLACE_COMMAND) + chr(0)
	send_and_check(instruction_packet,timeout = PLACE_COMMUNICATION_TIMEOUT_LIMIT)

def move(pos) : 
	global GO_TO_SERVO_POS
	GO_TO_SERVO_POS = pos
	rotate()