# ------------------ IDEAS -----------------------
Arduino Timer
Timer interrupt based servo PWM generation
Timer without interrupt servo PWM generation
# ------------------------------------------------

# ------------ TO DO -----------------------------
py_main.display_area_calc
lookup.lookup
arduino2 - exception_handling

accounts description

# ------------ INITIALIZATION FLOW ---------------

gui_init.py
	'''
	Initializes everything
	'''
	sets up the working directory for the entire project
	initialized GUI object
	import gui_main
	### calls py_main, which initializes the entire robot
	calls on_done to wrap things up before finishing execution of the program

gui_main.py 
	'''
	creates GUI
	'''
	import gui_objects.*
	import gui_maker.*
	declares password "glob_pass"
	import scara_sim

scara_sim.py
	'''
	intermediary between GUI and py_main
	performs all the checking w.r.t input from the gui, before calling py_main
	'''
	import py_main
	obtains number of available blocks for each alphabet

py_main.py
	import serial_ports_setup
	obtains arduino serial objects (instances of the Serial.serial class)
	import arduino1
	arduino1.init # handshake, and if true : global arduino1 = arduino1 object
	arduino1.dynamixel_initialization1 # power on dynamixel supply
	import dynamixel
		init() 
			check get connected dynamixel object from serial_ports_setup
			dynamixel_initializations # Dyna LED, Speed, ...
	arduino1.dynamixel_initialization2 # start checking LDR values
	import arduino2
	arduino2.init # set global object

	import lookup
		init_lookup() 	# read text file and parse it to obtain the
						# last saved positions for every block

serial_ports_setup.py
	'''
	defines a number of methods for obtaining serial objects pertaining
	to physical ports connected to the two arduino's and dynamixel
	'''
	import exception_handling

	def get_connected_arduino_objects() : 
		'''
		returns a list containing two serial objects, each representing
		a connected arduino device
		'''
		global serial_objects_list = get_available_serial_objects()
		get_connected_arduino_ports()

	def get_connected_arduino_ports() : 
		handshake with arduino1

# ------------------------------------------------


# ----------------- GUI FLOW ---------------------

MAIN window is displayed (initialized in gui_main after returning from py_main)
set RUN_WINDOW_CREATOR as callback method for button press for RUN

ON KEYPRESS (RUN) 
	withdraw the current window
	RUN window is displayed

after typing an input and pressing (Okay)
	scara_sim.check_string()  	# check if valid string based on number of available blocks
								# for each alphabet, invalid characters, ...
	GUI updated 
		POSSIBILITY 1) 
			Error message box is shown for entering invalid string
		POSSIBILITY 2) 	
			New (UPDATE) window is created with a (Quit) button created
			scara_sim.py_main 
				update CURRENT_ARRAY
				modify_blocks()

def py_main.modify_blocks() : 
	display_area_calc()
	for every element in CURRENT_ARRAY_ : 
		update label
		# -------- PICK UP BLOCK FROM POSITION -------------
		lookup.lookup(character name (example : "a"))	# updates LOOKUP_OUTPUT to represent dynamixel1, 
														# dynamixel2, and gripper servo rotations required
														# to pick up the closest possible (character name) 
														# block 
		move dynamixel-1 to position lookup.LOOKUP_OUTPUT[0]
		move dynamixel-2 to position lookup.LOOKUP_OUTPUT[1] 
		move gripper (ROTATE) to position lookup.LOOKUP_OUTPUT[2]
		arduino2.pick()
		# -------------------------------------------------

		# ------- PLACE BLOCK IN DISPLAY AREA -------------
		update label
		move dynamixel-1 to position DISPLAY_AREA_POSITIONS[i][0] # i represents the index of the current block
		move dynamixel-2 to position DISPLAY_AREA_POSITIONS[i][1]
		move gripper (ROTATE) to position DISPLAY_AREA_POSITIONS[i][2]
		arduino2.place()		
		# -------------------------------------------------

	for every block in display area : 
		execution similar to that above

	print('bring it on')

def display_area_calc() : 
	update DISPLAY_AREA_POSITIONS

def lookup.lookup() : 
	sort()
		# updates LOOKUP_OUTPUT to represent dynamixel1, 
		# dynamixel2, and gripper servo rotations required
		# to pick up the closest possible (character name)Í
		update LOOKUP_OUTPUT[0]
		update LOOKUP_OUTPUT[1]
		update LOOKUP_OUTPUT[2]

# -----------------------------------------------------------

# ----------- dynamixel.dyna_move() flow --------------------

