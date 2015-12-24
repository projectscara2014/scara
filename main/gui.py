import sys

WORKING_DIRECTORY = ''

# def setup(module_name) :
# 	global WORKING_DIRECTORY
# 	if __name__ == '__main__' : 
# 		working_directory = locate_file()
# 		WORKING_DIRECTORY = working_directory
# 		sys.path.append(WORKING_DIRECTORY)
# 		def make_terminal_compatible(working_directory) : 
# 			return_string = ''
# 			for character in working_directory : 
# 				if character == ' ' :
# 					return_string += '\{}'.format('')
# 				return_string += character
# 			return return_string

# 		os.chdir(working_directory)
# 		print(os.getcwd())
# 		working_directory = make_terminal_compatible(working_directory)
# 		print(working_directory)

# 		print(os.system('cd ' + working_directory))
# 		print(os.system('python run.py'))
# 	else : 
# 		print('called by ' + module_name)

# setup(__name__)

def setup() : 

	def locate_working_directory() : 
		working_directory = ''
		for element in __file__.split('/')[:-2] :
			working_directory += element + '/'
		return working_directory
	
	global WORKING_DIRECTORY
	WORKING_DIRECTORY = locate_working_directory()
	print('working_directory --> ',WORKING_DIRECTORY)
	sys.path.append(WORKING_DIRECTORY)

setup()

EXCEPTION_MODULE = 'none'
EXCEPTION = 'none'

def exception_caught(*args) :
	print(args)
	global EXCEPTION,EXCEPTION_MODULE

	'''
	important code to be added pertaining to exception handling here
	just printing exceptions for the time being
	'''

	print(EXCEPTION_MODULE + ' --> ' +EXCEPTION)
	print('printing complete')
	print()

from main import lookup
from main import dynamixel
from subordinate import exception_handling