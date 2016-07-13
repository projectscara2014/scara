import sys
gui = sys.modules["__main__"]

from utils.debug import debug
from utils.string_handling import *

if sys.platform.startswith('win') : 
	SYSTEM_PATH_SEPERATOR = '\\'
elif sys.platform.startswith('darwin') : 
	SYSTEM_PATH_SEPERATOR = '/'

LOOKUP_OUTPUT = [0,0,0]
DYNA_1_POS = 0
DYNA_2_POS = 0
#POSITION_ARRAY = [[[-15,-105,-15,-105,38,83,1],[-60,80,2,-40,48,84,1],[80,-92,-2,85,58,85,1]]]
POSITION_ARRAY = []
POSITION_ARRAY_FLAGS = []

max_scalable_area = 3072

@debug()
def lookup(letter,directive):
	#directive = 0 for pick and 1 for place
	###direction = 0 for fwd and 1 for bckwrd
	#letter needs to be local
	#directive needs to be local

	global LOOKUP_OUTPUT #delete later

	if (letter == "C"):
		sort(0,directive)
		# for A, index is 0
	if (letter == "A"):
		sort(1,directive)
	if (letter == "S"):
		sort(2,directive)
	if (letter == "R"):
		sort(3,directive)

	# CHANGE CHANGE CHANGE

@debug()
def sort(index,directive):
	#directive needs to be local
	global POSITION_ARRAY
	global POSITION_KEY

	# len_letters = len(POSITION_ARRAY)   #length of letters
	no_of_instances = len(POSITION_ARRAY[index])
	maximum = []
	for i in range(no_of_instances*2) :  
		maximum.append([])
	#loop to find maximums
	for i in range (no_of_instances):
		for j in range (2):
			if ( POSITION_ARRAY_FLAGS[ index ][ i ] != directive ):
				#checking availability

				#print("i = ",i," j = ",j)

				x = POSITION_ARRAY[ index ][ i ][ (j*2) +0 ]
				y = POSITION_ARRAY[ index ][ i ][ (j*2) +1 ]
				maximum[(2*i)+j] = max_of_two(x,y)
				#print("max[",(2*i)+j,"] = ",maximum[(2*i)+j])

			else :
				maximum[(2*i)+j] = max_scalable_area
				#max value possible
	
	# to find minimum
	i_min = 0
	j_min = 0
	for i in range (no_of_instances):
		for j in range (2):
			if(maximum[(2*i)+j] < maximum[(2*i_min)+j_min]):
				i_min = i
				j_min = j

	LOOKUP_OUTPUT[0] = POSITION_ARRAY[ index ][ i_min ][ (2*j_min) ]
	LOOKUP_OUTPUT[1] = POSITION_ARRAY[ index ][ i_min ][ (2*j_min) + 1 ]
	LOOKUP_OUTPUT[2] = POSITION_ARRAY[ index ][ i_min ][ j_min + 4 ]
	POSITION_ARRAY_FLAGS[ index ][ i_min ] = directive
	change_array(POSITION_ARRAY_FLAGS,0)

#@debug()
def max_of_two(x,y):
	global DYNA_1_POS
	global DYNA_2_POS
	a = mod(DYNA_1_POS - x)      	 #difference 1
	b = mod(DYNA_2_POS - y)       	 #difference 2
	if (a<b):
		a=b                       	 #if b is greater
	return a

#@debug()
def mod(s):
	if (s<0):
		s*=-1
	return s                        #make positive

######### ARRAY OPERATIONS ###########
def change_array(array,num):
	#num=0 ==> POSITION_ARRAY_FLAGS
	#num=1 ==> DISPLAY_AREA_POSITIONS
	with open(gui.WORKING_DIRECTORY + 'core' + SYSTEM_PATH_SEPERATOR + 'variable_array.txt','r') as variable_array: 
		k=[]
		for line in variable_array:
			k.append(line)
	
	s = str(array)
	if(num != len(k)-1):
		s += '\n'
	k[num] = s
	
	with open(gui.WORKING_DIRECTORY + 'core' + SYSTEM_PATH_SEPERATOR + 'variable_array.txt','w') as variable_array :
		for i in range(len(k)):
			variable_array.write(k[i])
########### RIYANSH CODES ##########

def init_lookup() :

	def edit_position_array(logs) :
		global POSITION_ARRAY
		global POSITION_ARRAY_FLAGS

		character_array = [] # list of characters : "a" or "b" or ...
		array = [] 	# list of strings in the lookup.txt corresponding to 
					#characters in character_array
		i = 0

		while(i < len(logs)) :

			i += skip_useless(logs,i)

			#if reached end of file/
			if(logs[i] == 'eof') :
				break
			#if commented line
			if(logs[i] == '#') :
				i += skip_until_character(logs,'\n',i)
				break

			#first character of a line : "a" or "b" or ...
			character_array.append(logs[i])
			i += skip_until_character(logs,'{',i)
			i += 1

			string = ''
			while(logs[i] != '}') :
				string += logs[i]
				i += 1
			i += 1

			array.append(string)
			if(i < len(logs)) :
				i += skip_useless(logs,i)
			else :
				break

		#character_array and array lists are filled
		for i in range(len(array)) :
			array[i] = remove_useless(array[i])

		def decode_array(array) :
			'''
			isolate strings pertaining to each block for a character
			returns an array of arrays that consist of strings, corresponding
			to each block
			'''
			return_array = []
			for i in range(len(array)) :
				return_array.append([])
			for i in range(len(array)) :
				j = 0
				while(j < len(array[i])) :
					skip_useless(array[i],j)
					skip_character(array[i],',',j)
					j += skip_until_character(array[i],'[',j)
					j += 1
					string = ''
					while(array[i][j] != ']') :
						string += array[i][j]
						j += 1
					j += 1
					return_array[i].append(string)
			return(return_array)

		array = decode_array(array)

		#create a list of lists consisting of empty lists 
		#[ [ [],[],...],...]
		return_array = []
		for i in range(len(array)) :
			return_array.append([])
			for j in range(len(array[i])) :
				return_array[i].append([])

		#fill the return_array
		for i in range(len(array)) :
			for j in range(len(array[i])) :
				k = 0
				#fill the empty arrays with numbers (as strings)
				while(k < len(array[i][j])) :
					string = ''
					while((k < len(array[i][j])) and (array[i][j][k] != ',')and(array[i][j][k] != '\n')) :
						string += array[i][j][k]
						k += 1
					k += 1

					return_array[i][j].append(string)

		array = return_array

		#convert the integers (as strings) in return array to integers
		return_array = []
		for i in range(len(array)) :
			return_array.append([])
			for j in range(len(array[i])) :
				return_array[i].append([])

		for i in range(len(array)) :
			for j in range(len(array[i])) :
				for k in range(len(array[i][j])) :
					return_array[i][j].append(string_to_int(array[i][j][k]))

		#------

		POSITION_ARRAY = return_array

		for character in POSITION_ARRAY :
			array = []
			for element in character :
				array.append(element.pop())
			POSITION_ARRAY_FLAGS.append(array)

	with open(gui.WORKING_DIRECTORY + 'core' + SYSTEM_PATH_SEPERATOR + 'lookup.txt','r') as logs :
		logs_ = logs.read()
		edit_position_array(logs_)
		logs.close()

######### Initialization call #########

init_lookup()
print("Position array :- ",POSITION_ARRAY)
print
print('position array flags : ',POSITION_ARRAY_FLAGS)
print
change_array(POSITION_ARRAY_FLAGS,0)