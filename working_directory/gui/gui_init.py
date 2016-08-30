import sys

WORKING_DIRECTORY = ''
SPLITTING_CHARACTER = ''
if sys.platform.startswith('win') : 
	SPLITTING_CHARACTER = '\{}'.format('')
elif sys.platform.startswith('darwin') : 
	SPLITTING_CHARACTER = '/'


def setup() : 
	'''
	Sets up the working directory for the entire project
	'''

	def locate_working_directory() : 
		working_directory = ''
		for element in __file__.split(SPLITTING_CHARACTER)[:-2] :
			working_directory += element + '{}'.format(SPLITTING_CHARACTER)
		return working_directory
	
	global WORKING_DIRECTORY
	WORKING_DIRECTORY = locate_working_directory()
	print('working_directory --> ',WORKING_DIRECTORY)
	sys.path.append(WORKING_DIRECTORY)

def on_done() :
	'''
	Takes care of wrapping up everything before exiting the program
	'''
	gui_main.scara.py_main.arduino1.initialize_to_default()

	# CHANGE  --- Everything else

setup()

from gui import gui_main

from gui import gui_exception_handling

print("All modules imported")
gui_main.scara.py_main.init()
gui_main.scara.init()

m = gui_main.MAIN()		# initializes GUI object

on_done() 