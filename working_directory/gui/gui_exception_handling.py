import sys

gui_init_module = sys.modules['__main__']

py_main_module = gui_init_module.gui_main.scara.py_main
arduino1 = py_main_module.arduino1
arduino2 = py_main_module.arduino2
dynamixel = py_main_module.dynamixel

def print_karo():
	print("PRINT KARO NA")
	py_main_module.print_karo()

# ------ arduino1 related functions ----------
def arduino1_disconnected():
	print('Exception : arduino1_disconnected')

# def arduino1_not_responding() :
# 	print('Exception : arduino1_not_responding')

def arduino1_brownout_12V() : 
	print('Exception : arduino1_brownout_12V')
	sys.exit(1)

def arduino1_brownout_5V() : 
	print('Exception : arduino1_brownout_5V')
	sys.exit(1)

def arduino1_dynamixel2_disconnected() : 
	print('Exception : arduino1_dynamixel2_disconnected')
	sys.exit(1)

def arduino1_dynamixel_1_and_2_disconnected() : 
	print('Exception : arduino1_dynamixel_1_and_2_disconnected')
	sys.exit(1)

def arduino1_command_not_understood() : 
	print('Exception : arduino1_command_not_understood')
	raise RuntimeError("Incorrect protocol ==> Arduino 1")
	sys.exit(1)

# ---------------------------------------------

# -------- arduino2 related functions ---------
def arduino2_disconnected():
	print('Exception : arduino2_disconnected')
# def arduino2_not_responding() :
# 	print('Exception : arduino2_not_responding')
# ---------------------------------------------

# -------- dynamixel related functions --------
def dynamixel_not_responding() :
	print('Exception : dynamixel_not_responding')
	sys.exit(1)

def dynamixel_did_brownout_occur():
	print('Exception : dynamixel_did_brownout_occur')
	arduino1.get_status()

# ---------------------------------------------

# --- serial_ports_setup related functions ---- 
def serial_ports_setup_dynamixel_not_connected() : 
	print('Exception : serial_ports_setup_dynamixel_not_connected')
	sys.exit(1)

def serial_ports_setup_arduino1_not_connected() : 
	print('Exception : serial_ports_setup_arduino1_not_connected')
	sys.exit(1)

def serial_ports_setup_arduino2_not_connected() : 
	print('Exception : serial_ports_setup_arduino2_not_connected')
	# TEMP
	sys.exit(1)
# ---------------------------------------------

# # -------- lookup related functions ----------
# # --------------------------------------------

# - status_packet_handling related functions -
def status_packet_handling_input_voltage_error() : 
	arduino1.initialize_to_default()
	print('Exception : status_packet_handling_input_voltage_error')
	sys.exit(1)

def status_packet_handling_angle_limit_error() : 
	arduino1.initialize_to_default()
	print('Exception : status_packet_handling_angle_limit_error')
	sys.exit(1)

def status_packet_handling_overheating_error() :
	arduino1.initialize_to_default()
	print('Exception : status_packet_handling_overheating_error')
	sys.exit(1)

def status_packet_handling_range_error() :
	arduino1.initialize_to_default()
	print('Exception : status_packet_handling_range_error')
	sys.exit(1)

def status_packet_handling_checksum_error() : 
	print('Exception : status_packet_handling_checksum_error')
	sys.exit(1)

def status_packet_handling_overload_error() : 
	arduino1.initialize_to_default()
	print('Exception : status_packet_handling_overheting_error')
	sys.exit(1)

def status_packet_handling_instruction_error() : 
	print('Exception : status_packet_handling_instruction_error')
	sys.exit(1)

def status_packet_handling_invalid_error_byte_error() : 
	arduino1.initialize_to_default()
	print('Exception : status_packet_handling_invalid_error_byte_error')
	sys.exit(1)
# -------------------------------------------

# ------- py_main related funcitons ---------
# -------------------------------------------