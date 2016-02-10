#------------------------------------ SETUP ----------------------------------------------
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
	print('working_directory --> ',WORKING_DIRECTORY)
	sys.path.append(WORKING_DIRECTORY)

setup()

#---------------------- DYNAMIXEL AND ARDUINO CONTROLLING FUNCITONS -----------------------------

from main_directory import dynamixel
from main_directory import arduino2
from main_directory import lookup
import this_to_that

def print_dynamixel_position() : 
	print("dynamixel 1 position --> {0}".format(dynamixel.GO_TO_DYNA_1_POS))
	print("dynamixel 2 position --> {0}".format(dynamixel.GO_TO_DYNA_2_POS))

def move_dynamixel(dynamixel_1_movement=0,dynamixel_2_movement=0) : 
	dynamixel.GO_TO_DYNA_1_POS += dynamixel_1_movement
	dynamixel.GO_TO_DYNA_2_POS += dynamixel_2_movement
	dynamixel.dyna_move()

def move_servo(servo_movement) :
	arduino2.GO_TO_SERVO_POS += servo_movement
	arduino2.write()

def print_everything() : 
	text.insert('end','dynamixel_movement_per_command --> {0}\nservo_movement_per_command --> {1}\n'.\
		format(dynamixel_movement_per_command,servo_movement_per_command))
	text.insert('end','dynamixel1 --> {0}\ndynamixel2 --> {1}\n'.\
		format(dynamixel.GO_TO_DYNA_1_POS,dynamixel.GO_TO_DYNA_2_POS))
	text.insert('end','servo_hand --> {0}\n'.format(arduino2.GO_TO_SERVO_POS))
	text.insert('end','\n')

#---------------------- TKINTER RELATED FUNCTIONS ---------------------------------------------
import Tkinter as tk
dynamixel_movement_per_command = 1
servo_movement_per_command = 1
FLAG = 0

def do_nothing(event) : 
	pass

def on_key_press(event):
	
	global DYNA_POS_1,DYNA_POS_2
	dynamixel_movement_per_command = 1
	servo_movement_per_command = 1

	def char_to_int(character) :
		for i in range(256) :
			if chr(i) == character :
				return i
		return 256

	def move(keypress) :
		global dynamixel_movement_per_command,servo_movement_per_command

		print_everything()

		if(keypress == 113) :
			# "q" pressed
			move_dynamixel(dynamixel_1_movement = -1 * dynamixel_movement_per_command)
		elif keypress == 119 :	
			# "w" pressed
			move_dynamixel(dynamixel_1_movement = +1 * dynamixel_movement_per_command)
		elif(keypress == 97) :
			# "a" pressed
			move_dynamixel(dynamixel_2_movement = -1 * dynamixel_movement_per_command)
		elif keypress == 115 :	
			# "s" pressed
			move_dynamixel(dynamixel_2_movement = +1 * dynamixel_movement_per_command)
		elif keypress == 122 :
			# "z" pressed
			if arduino2.GO_TO_SERVO_POS > 0 :
				move_servo(-1 * servo_movement_per_command)
		elif keypress == 120 :
			# "x" pressed
			if arduino2.GO_TO_SERVO_POS < 180 :
				move_servo(+1 * servo_movement_per_command)
		elif keypress == 101 :
			# "e" pressed
			dynamixel_movement_per_command += 1
		elif keypress == 100 :
			# "d" pressed
			if dynamixel_movement_per_command > 1:
				dynamixel_movement_per_command -= 1
		elif keypress == 114 :
			# "r" pressed
			servo_movement_per_command += 1
		elif keypress == 102 :
			# "f" pressed
			if servo_movement_per_command > 1 :
				servo_movement_per_command -= 1
		elif keypress == 112 :
			# "p" pressed
			root.destroy()

		else :
			print('INVALID KEY PRESSED')
		
	keypress = char_to_int(event.char)
	move(keypress)
	print(dynamixel_movement_per_command)
	print(servo_movement_per_command)
	# root.bind('<KeyPress>',do_nothing)

root = tk.Tk()
root.geometry('600x400')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', on_key_press)

def block_position_setup() : 
	#blocks = lookup.some_function()
	def setup_one_block() : 
		root.bind('<KeyPress>',on_key_press)
		root.mainloop()
		entire_block_position_list = this_to_that.calculate_entire_block_position_list(dynamixel.GO_TO_DYNA_1_POS,\
			dynamixel.GO_TO_DYNA_2_POS,arduino2.GO_TO_SERVO_POS)
		with open('saved_positions.txt','w') as f:
			f.write(str(entire_block_position_list) + '\n')
	setup_one_block()

block_position_setup()
print('and continuing ...')


