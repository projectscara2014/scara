from subordinate_directory import serial_ports_setup
arduino = serial_ports_setup.find_dynamixel_and_arduino()
# import serial
# arduino = serial.Serial('/dev/cu.usbmodem1421')
arduino.baudrate = 57600
GO_TO_SERVO_POS = 0

def write() :
	global GO_TO_SERVO_POS 
	instruction_packet = '\x00' + chr(GO_TO_SERVO_POS)
	arduino.write(instruction_packet)
	
def pick() : 
	arduino.write('\x01')
	pass

def place() : 
	arduino.write('\x02')
	pass