import sys
import inspect

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
gui_init_module = sys.modules['__main__']

from utils import error_logging


def log_error(module_name,exception_name) : 
	error_logging.log(module_name + '--> ' + exception_name)

def handle_exception(exception_name,*args):
	module_name = inspect.stack()[1][1].split("\\")[-1].split(".")[0]

	executable_string = "gui_init_module.gui_exception_handling." + module_name + "_" + exception_name + "(*args)"
	print(executable_string)

	log_error(module_name,exception_name)
	try : 
		exec(executable_string)
	except NameError : 
		print('invalid exception')  # CHANGE -- Let GUI print this in a msg box
		sys.exit(0) # CHANGE -- delete

def handle_exception_old(module_name,exception_name,*args) :
	
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
	
# handle_exception('arduino1','12V brownout')

# # ----- TESTING -- Delete later --------
# def exception_handling_testing_errr(*args):
# 	print("Heyyy")
# 	print(str(args))

# handle_exception("testing_errr",1)
# # -------------------------------------