import os

def locate_file() : 
    working_directory = ''
    for element in __file__.split('/')[:-1] :
        working_directory += element + '/'
    return working_directory

os.chdir(locate_file())

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
	#some_file.n = int(args[0])

print('-----------------------------------')

import some_file
some_file.do_some_work()