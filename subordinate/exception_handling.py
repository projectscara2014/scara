import sys
gui = sys.modules['__main__']
from subordinate import error_logging # log

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
	print('exception called by --> ' + module_name)
	
	if module_name in module_names.keys() and\
		exception_name in module_names[module_name] :
		
		gui.EXCEPTION_MODULE = module_name
		print(gui.EXCEPTION_MODULE)
		gui.EXCEPTION = exception_name
		error_logging.log(module_name + ' : ' + exception_name)
		gui.exception_caught(*args)
		
	else : 
		print('invalid exception')
		print()


error_logging.log('rana here')