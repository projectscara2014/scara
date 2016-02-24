import serial
import time
arduino = serial.Serial('/dev/cu.usbmodem1411')

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
		else :
			print('hallaleuja')
	serial_object.write = decorator(serial_object.write)
	serial_object.read = decorator(serial_object.read)
	serial_object.inWaiting = decorator(serial_object.inWaiting)
	serial_object.set_baudrate = set_baudrate
	return serial_object

arduino = decorate_serial_object(arduino)
print('zzzzzz')
time.sleep(5)
arduino.set_baudrate(57600)
print(arduino.write)
print(arduino.read)