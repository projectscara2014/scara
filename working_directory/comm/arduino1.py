import serial
import time
import sys

global arduino1

global send_and_check_count
global known_error_packets
global last_sent_command

known_error_packets = ['B','b','1','2','x']
# B --> 12V brownout
# b -->  5V brownout
# 1 --> Dynamixel 1 & 2 disconnected
# 2 --> Dynamixel 2 disconnected
# x --> Command not understood

def init(arduino1_serial_object):
	global arduino1
	arduino1 = arduino1_serial_object
	initialize_to_default()
	if(not send_and_check('h','0')):
		print("WRONG ARDUINO INITIALIZED")
		sys.exit(0)
		# CHANGE --- EH Arduino 1 disconnected
	
def initialize_to_default():
	'''
	Sends command to RESET Base Station 1
	'''
	if(not send_and_check('I','i')):
		print("ERROR in arduino_initialization @arduino1.py")
		sys.exit(0)

def dynamixel_initialization1():
	# CHANGE --- Add exceptions throughout the function
	if(not send_and_check('D','d')):
		print("ERROR in dynamixel_initialization @arduino1.py")
		sys.exit(0)
		# CHANGE --- EH Arduino 1 disconnected
	time.sleep(5)

def dynamixel_initialization2():
	if(not send_and_check('L','l')):
		print("ERROR in dynamixel_initialization @arduino1.py")
		sys.exit(0)
	# if not ok, exception

def get_status():
	last_sent_command = 'S' # For servicing when 'x' is sent
	recieved_packet = send_and_recieve('S')
	if(recieved_packet != 'o'):
		service_arduino1_error_packets(recieved_packet)
	else:
		print("All OK")
def send_and_check(outgoing_packet,expected_packet):
	global send_and_check_count
	global last_sent_command

	last_sent_command = outgoing_packet
	send_and_check_count = 10
	return _send_and_check_(outgoing_packet,expected_packet)

def _send_and_check_(outgoing_packet,expected_packet):
	global send_and_check_count
	global known_error_packets
	return_val = False

	print("py_to_arduino1 ---> "+outgoing_packet)
	recieved_packet = send_and_recieve(outgoing_packet)
	print("arduino1_to_py ---> "+recieved_packet)
	if(recieved_packet == expected_packet):
		print("recieved_packet matches expected_packet")
		return_val = True
	elif(recieved_packet in known_error_packets):
		print("known_error_packet recieved")
		return_val = service_arduino1_error_packets(recieved_packet)
	elif(send_and_check_count != 0):
		send_and_check_count -= 1
		print("send_and_check_count = "+str(send_and_check_count))
		time.sleep(0.5)
		return_val = _send_and_check_('R',expected_packet)
	else:
		print("communication not successful")
	
	return return_val

def send_and_recieve(data_packet):
	global arduino1
	clear_buffer()
	arduino1.write(data_packet)
	time.sleep(0.1)
	return get_recieving_packet()

def clear_buffer():
	if(arduino1.inWaiting()>0):
		recieved_packet = arduino1.read(arduino1.inWaiting())

def get_recieving_packet():
	recieved_packet = 'None'
	for i in range(50):
		if(arduino1.inWaiting()>0):
			recieved_packet = arduino1.read(1)
			break
	return recieved_packet

def service_arduino1_error_packets(recieved_packet):
	return_val = False
	print("Service routine called:- Have to service --> "+recieved_packet)
	print("ARDUINO1.PY ERROR ===>"),
	if(recieved_packet == 'B'):
		print("12V supply brownout occured")
	elif(recieved_packet == 'b'):
		print("5V supply brownout occured")
	elif(recieved_packet == '1'):
		print("Dynamixel 1 and 2 disconnected")
	elif(recieved_packet == '2'):
		print("Dynamixel 2 disconnected")
	elif(recieved_packet == 'x'):
		return_val = send_and_recieve(last_sent_command)
		print("Incorrect protocol")

	return return_val
	# CHANGE