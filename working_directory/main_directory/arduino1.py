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

	recieved_packet = send_and_recieve('I')
	print("py2arduino ---> 'I' ")
	
	if(recieved_packet == 'i'):
		print("arduino2py ---> 'i'")
	else:
		recieved_packet = send_and_recieve('R') #Repeat packet
		print("py2arduino ----> 'R'")
		if(recieved_packet == 'i'):
			print("arduino2py ---> 'i'")
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
	for i in range(500):
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


