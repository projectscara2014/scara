import serial
import time
from subordinate_directory import serial_ports_setup
import sys

global arduino1

def init():
	global arduino1
	arduino1 = serial_ports_setup.find_dynamixel_and_arduino()
	arduino1.baudrate = 57600
	initialize_to_default()
	
def initialize_to_default():
	time.sleep(2)
	send_and_check('I','i')

def dynamixel_initialization():
	send_and_check('D','d')
	# send command to switch on relay
		# check for brown out at 12v
		# switch on relay if all is good
		# if all not good, send -- 'n'
		# start checking for brownout at 12v
		# 'expe cted_data_packet' = 'L'
		# send acknowledgement packet -- 'd'
	# wait for acknowledgement -- 'd'
	# wait for some time till dynamixel is initialized
	# send LED--ON command to dynamixel.
	# if error, send command to switch off relay
	# if no error, send 'L' to switch on LDR checking

def send_and_check(outgoing_packet,expected_packet,delay_val = 0):
	recieved_packet = send_and_recieve(outgoing_packet)
	print("py2arduino ---> "+outgoing_packet)
	time.sleep(delay_val)
	if(recieved_packet == expected_packet):
		print("arduino2py ---> "+expected_packet)
	else:
		recieved_packet = send_and_recieve('R') #Repeat packet
		print("py2arduino ----> 'R'")
		if(recieved_packet == expected_packet):
			print("arduino2py ---> "+expected_packet)
		else:	
			print("communication not successful")
			# CHANGE

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

print("\n------>\n")
init()
# time.sleep(5)
dynamixel_initialization()
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


