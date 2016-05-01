import sys

WORKING_DIRECTORY = ''
SPLITTING_CHARACTER = ''
if sys.platform.startswith('win') : 
	SPLITTING_CHARACTER = '\{}'.format('')
elif sys.platform.startswith('darwin') : 
	SPLITTING_CHARACTER = '/'


def setup() : 

	def locate_working_directory() : 
		working_directory = ''
		for element in __file__.split(SPLITTING_CHARACTER)[:-2] :
			working_directory += element + '{}'.format(SPLITTING_CHARACTER)
		return working_directory
	
	global WORKING_DIRECTORY
	WORKING_DIRECTORY = locate_working_directory()
	sys.path.append(WORKING_DIRECTORY)

setup()

import sys
gui = sys.modules['__main__']
from utils import error_logging

# arduino1 related functions
def arduino1_not_responding() :
	print('Exception : arduino1_not_responding')

def brownout_12V() : 
	print('Exception : brownout_12V')

def brownout_5V() : 
	print('Exception : brownout_5V')

def dynamixel2_disconnected() : 
	print('Exception : dynamixel2_disconnected')

def dynamixel_1_and_2_disconnected() : 
	print('Exception : dynamixel_1_and_2_disconnected')

def command_not_understood() : 
	print('Exception : command_not_understood')

# arduino2 related functions
def arduino2_not_responding() :
	print('Exception : arduino2_not_responding')

# dynamixel related functions
def dynamixel_not_responding() :
	print('Exception : dynamixel_not_responding')

# serial_ports_setup related functions : 
def dynamixel_not_connected() : 
	print('Exception : dynamixel_not_connected')

def arduino1_not_connected() : 
	print('Exception : arduino1_not_connected')

def arduino2_not_connected() : 
	print('Exception : arduino2_not_connected')

# lookup related functions

# status_packet_handling related functions
def input_voltage_error() : 
	print('Exception : input_voltage_error')

def angle_limit_error() : 
	print('Exception : angle_limit_error')

def overheating_error() :
	print('Exception : overheating_error')

def range_error() :
	print('Exception : range_error')

def checksum_error() : 
	print('Exception : checksum_error')

def overload_error() : 
	print('Exception : overheting_error')

def instruction_error() : 
	print('Exception : instruction_error')

def invalid_error_byte_error() : 
	print('Exception : invalid_error_byte_error')

# py_main related funcitons

def handle_exception(module_name,exception_name,*args) :
	
	# ---------- modules and corresponding exceptions -----------
	arduino1 = {
		'arduino not responding':arduino1_not_responding,
		'12V brownout':brownout_12V,
		'5V brownout':brownout_5V,
		'dynamixel2 disconnected':dynamixel2_disconnected,
		'dynamixel 1 and 2 disconnected':dynamixel_1_and_2_disconnected,
		'command not understood':command_not_understood}

	arduino2 = {
		'arduino not responding':arduino2_not_responding}

	dynamixel = {
		'dynamixel not responding':dynamixel_not_responding}
	
	serial_ports_setup = {
		'dynamixel not connected':dynamixel_not_connected,
		'arduino1 not connected':arduino1_not_connected,
		'arduino2 not connected':arduino2_not_connected
	}

	lookup = {}
	
	status_packet_handling  = {
		'input voltage error':input_voltage_error,
		'angle limit error':angle_limit_error,
		'overheating error':overheating_error,
		'range error':range_error,
		'checksum error':checksum_error,
		'overload error':overload_error,
		'instruction error':instruction_error,
		'invalid error byte':invalid_error_byte_error}
	
	py_main = {}

	# ------------------------------------------------------------

	module_names = {
		'arduino1' : arduino1,
		'arduino2' : arduino2,
		'dynamixel' : dynamixel,
		'lookup' : lookup,
		'status_packet_handling' : status_packet_handling,
		'py_main' : py_main,
		'serial_ports_setup':serial_ports_setup
	}

	module_name = module_name.split('.')[-1]	# getting only the module names and not the entire path

	def log_error(module_name,exception_name) : 
		error_logging.log(module_name + '--> ' + exception_name)


	if module_name in module_names.keys() and\
		exception_name in module_names[module_name].keys() :
		# CHANGE -- Implement functions in GUI and call from here
		log_error(module_name,exception_name)
		exception_handling_function = module_names[module_name][exception_name]
		exception_handling_function()
	else : 
		print('invalid exception')
		sys.exit(1)
		# CHANGE -- Let GUI print this in a msg box
	
handle_exception('arduino1','12V brownout')