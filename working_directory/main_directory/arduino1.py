import serial
import time
from subordinate_directory import serial_ports_setup
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

def init():
	global arduino1
	arduino1 = serial_ports_setup.find_dynamixel_and_arduino()
	arduino1.baudrate = 57600
	initialize_to_default()
	
def initialize_to_default():
	time.sleep(2)
	send_and_check('I','i')

def dynamixel_initialization():
	if(not send_and_check('D','d')):
		print("ERROR in dynamixel_initialization @arduino1.py")
		sys.exit(0)
	# wait for dynamixel to intialize
	# tell dynamixel to switch on LED
	# if not Ok, exception
	# if OK, do the following
	send_and_check('L','l')
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

	print("py2arduino ---> "+outgoing_packet)
	recieved_packet = send_and_recieve(outgoing_packet)
	print("arduino2py ---> "+recieved_packet)
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
		if(recieved_packet == 'x'):
			print("PROTOCOL ERROR")		
			sys.exit(0)

def get_recieving_packet():
	recieved_packet = 'None'
	for i in range(50):
		if(arduino1.inWaiting()>0):
			recieved_packet = arduino1.read(1)
			if(recieved_packet == 'x'):
				print("PROTOCOL ERROR")		
				sys.exit(0)
			else:
				break
	return recieved_packet

def service_arduino1_error_packets(recieved_packet):
	return_val = False
	print("have to service -- "+recieved_packet)
	if(recieved_packet == 'B'):
		print("ERROR ===> 12V supply brownout occured")
	elif(recieved_packet == 'b'):
		print("ERROR ===> 5V supply brownout occured")
	elif(recieved_packet == '1'):
		print("ERROR ===> Dynamixel 1 and 2 disconnected")
	elif(recieved_packet == '2'):
		print("ERROR ===> Dynamixel 2 disconnected")
	elif(recieved_packet == 'x'):
		return_val = send_and_recieve(last_sent_command)

	return return_val
	# CHANGE

print("\n------>\n")
init()
dynamixel_initialization()
get_status()

print("\n------>\n")
sys.exit(0)



# def wait_for(word,msg_type):
# 	global arduino1
# 	return_val = False
# 	for i in range(5000):
		# if(arduino1.inWaiting()==len(word)):
		# 	message = arduino1.read(len(word))
# 			return_val = decode_message(message,word,msg_type)
# 	return return_val

# def decode_message(message,word,msg_type):
# 	return_val = False
# 	if(msg_type == 1): # word == message
# 		if(word == message):
# 			return_val = True
# 	return return_val


