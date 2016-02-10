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
from main_directory import lookup

def print_dynamixel_position() : 
	print("dynamixel 1 position --> {0}".format(dynamixel.GO_TO_DYNA_1_POS))
	print("dynamixel 2 position --> {0}".format(dynamixel.GO_TO_DYNA_2_POS))

def move_dynamixel(dynamixel_1_movement=0,dynamixel_2_movement=0) : 
	dynamixel.GO_TO_DYNA_1_POS = dynamixel.GO_TO_DYNA_1_POS + dynamixel_1_movement
	dynamixel.GO_TO_DYNA_2_POS = dynamixel.GO_TO_DYNA_2_POS + dynamixel_2_movement
	dynamixel.dyna_move()

#---------------------- TKINTER RELATED FUNCTIONS ---------------------------------------------
import Tkinter as tk

def do_nothing() : 
	pass

def on_key_press(event):
	
	global DYNA_POS_1,DYNA_POS_2
	def char_to_int(character) :
		for i in range(256) :
			if chr(i) == character :
				return i
		return 256

	def move(keypress) :
		global DYNA_POS_1,DYNA_POS_2

		if(keypress == 113) :
			# "q" pressed
			move_dynamixel(dynamixel_1_movement = -1)
		elif keypress == 119 :	
			# "w" pressed
			move_dynamixel(dynamixel_1_movement = +1)
		elif(keypress == 97) :
			# "a" pressed
			move_dynamixel(dynamixel_2_movement = -1)
		elif keypress == 115 :	
			# "s" pressed
			move_dynamixel(dynamixel_2_movement = +1)
		else :
			print('press either "q","w","a","s"')

	text.insert('end','current dynamixel positions : \n dynamixel1 --> {0}\ndynamixel2 --> {1}\n\n'.\
		format(dynamixel.GO_TO_DYNA_1_POS,dynamixel.GO_TO_DYNA_2_POS))
	
	keypress = char_to_int(event.char)
	move(keypress)
	root.bind('<KeyPress>',do_nothing)

root = tk.Tk()
root.geometry('600x400')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', on_key_press)