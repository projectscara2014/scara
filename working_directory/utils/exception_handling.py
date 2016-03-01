import sys
gui = sys.modules['__main__']
from utils import error_logging

def handle_exception(module_name,exception_name,*args) :
	
	arduino = ['arduino not responding','cant connect']
	dynamixel = ['dynamixel not responding','cant connect']
	lookup = []
	status_packet_handling  = ['input voltage error','angle limit error',\
	'overheting error','range error','checksum error','overload error',\
	'instruction error','invalid error byte']
	py_main = []

	module_names = {
		'arduino' : arduino,
		'dynamixel' : dynamixel,
		'lookup' : lookup,
		'status_packet_handling' : status_packet_handling,
		'py_main' : py_main,
	}

	module_name = module_name.split('.')[-1]

	if module_name in module_names.keys() and\
		exception_name in module_names[module_name] :
		print('Exception : ' + module_name + '--> ' + exception_name)
		error_logging.log(module_name + '--> ' + exception_name)
		# CHANGE -- Implement functions in GUI and call from here
		if(module_name == 'dynamixel' and exception_name == 'cant connect'):
			dynamixel_not_connected()
	else : 
		print('invalid exception')
		# CHANGE -- Let GUI print this in a msg box

def dynamixel_not_connected():
	print("*** dynamixel_not_connected() ***")
	print("display an error message or something in gui")
	sys.exit(1)