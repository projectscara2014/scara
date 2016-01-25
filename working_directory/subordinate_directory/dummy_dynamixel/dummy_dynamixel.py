import sys
SYSTEM_PATH_SEPERATOR = ''
if sys.platform.startswith('win') : 
	SYSTEM_PATH_SEPERATOR = '\{}'.format('')
elif sys.platform.startswith('darwin') : 
	SYSTEM_PATH_SEPERATOR = '/'

try : 
	from subordinate_directory import string_handling #char_to_int,skip_until_character
except : 
	WORKING_DIRECTORY = ''

	def setup() : 

		def locate_working_directory() : 
			working_directory = ''
			for element in __file__.split(SYSTEM_PATH_SEPERATOR)[:-2] :
				working_directory += element + '{}'.format(SYSTEM_PATH_SEPERATOR)
			return working_directory
		
		global WORKING_DIRECTORY
		WORKING_DIRECTORY = locate_working_directory()
		print('working_directory --> ',WORKING_DIRECTORY)
		sys.path.append(WORKING_DIRECTORY)
 
	setup()
	from subordinate_directory import string_handling #char_to_int,skip_until_character
else :
	import sys
	gui = sys.modules["__main__"]
	WORKING_DIRECTORY = gui.WORKING_DIRECTORY

from subordinate_directory import status_packet_handling #print_packet

class Dynamixel : 
	
	def __init__(self) :
		self.memory = self.read_memory()

		self.status_packet = []

		self.instruction_packet = []
		self.motor_id = ''
		self.instruction_packet_length = ''
		self.instruction= ''
		self.parameters = []
	
	def read(self,in_waiting) : 
		return_string = self.make_string_from_list(self.status_packet)
		self.status_packet = []
		# status_packet_handling.print_packet(return_string)
		return return_string
			
	def write(self,instruction_packet) : 
		# status_packet_handling.print_packet(instruction_packet)
		instruction_packet = list(instruction_packet)
		self.motor_id = instruction_packet[2]
		self.instruction_packet_length = instruction_packet[3]
		self.instruction = instruction_packet[4]
		self.parameters = instruction_packet[5:-1]
		self.status_packet.extend(self.build_status_packet())
		self.build_status_packet()
		# self.print_packet(self.status_packet)
		# if self.instruction == '\x03' and self.parameters[0] == '\x1e' : 
		# 	self.expected_position_low = self.parameeters[1]
		# 	self.expected_position_high = self.parameters[2]

	def inWaiting(self) : 
		return(len(self.status_packet))

	def build_status_packet(self) : 

		def not_checksum(l) :
			checksum = 0
			for i in range(len(l)) :
				checksum += l[i]
			not_checksum = (~checksum)&0xff
			return not_checksum

		status_packet = ['\xff','\xff']
		status_packet.append(self.motor_id)
		
		instructions_that_return_parameters = ['\x02']
		instructions_that_edit_memory = ['\x03']

		if self.instruction in instructions_that_edit_memory :
			starting_address = ord(self.parameters[0])
			for i in range(len(self.parameters[1:])) :
				self.memory[starting_address+i] = ord(self.parameters[1+i])
			self.update_dynamixel()
			# self.print_memory()

		if self.instruction in instructions_that_return_parameters : 
			#instruction returns parameters --> read
			starting_address = ord(self.parameters[0])
			length_of_data_to_be_read = ord(self.parameters[1])
			status_packet.append(chr(length_of_data_to_be_read+2))	#status packet length --> number_of_parameters + 2
			status_packet.append('\x00')	#error byte

			for i in range(length_of_data_to_be_read) : 
				try :
					status_packet.append(chr(self.memory[starting_address+i]))
				except : 
					status_packet.append('\x00')
			#return parameters --> check if starting address is 0x1E and return DYNA_POS_1 and DYNA_POS_2

		else :
			status_packet.append('\x02')	#status packet length
			status_packet.append('\x00')	#error byte
			
		checksum = []
		for i in range(2,len(status_packet)) : 
			checksum.append(ord(status_packet[i]))
		status_packet.append(chr(not_checksum(checksum)))
		return status_packet

	def update_dynamixel(self) : 
		for i in range(30,36) : 
			self.memory[i+6] = self.memory[i]

	def make_string_from_list(self,list_) : 
		return_string = ''
		for element in list_ : 
			return_string += str(element) 
		return return_string

	def read_memory(self) :
		'''
		returns a dictionary consisting of address:value pairs 
		as elements, simulating the dynamixel memory
		'''
		memory = {}
		text_memory = ''
		# with open(gui.WORKING_DIRECTORY + 'subordinate_directory' + SYSTEM_PATH_SEPERATOR + 'dummy_dynamixel' + SYSTEM_PATH_SEPERATOR + 'dymmy_dynamixel_memory.txt','r') as f : 
		with open(WORKING_DIRECTORY + 'subordinate_directory' + SYSTEM_PATH_SEPERATOR + 'dummy_dynamixel' + SYSTEM_PATH_SEPERATOR + 'dummy_dynamixel_memory.txt','r') as f : 
			text_memory = f.read()
		list_memory = []
		return_string = ''
		i=0
		while i < len(text_memory) :
			if text_memory[i] == '#' :
				i += string_handling.skip_until_character(text_memory,chr(13),i)
			
			if string_handling.char_to_int(text_memory[i]) != 13 :
				return_string += text_memory[i]
			else : 
				list_memory.append(return_string)
				return_string = ''
			i += 1

		temp_list_memory = []
		for line in list_memory : 
			if line != '' : 
				temp_list_memory.append(line)
		list_memory = temp_list_memory
		del temp_list_memory

		for line in list_memory :
			address = ''
			value = ''
			try : 
				address = int(line.split('	')[0].split(' ')[0])
			except ValueError : 
				if(line == '') :
					pass
				else : 
					raise ValueError
			else :
				try : 
					value = int(line.split('	')[1].split(' ')[0])
				except ValueError : 
					# value = 0
					value = '-'
			memory[address] = value

		return memory

	def write_memory(self,address,value) : 
		self.memory[address] = value
		self.print_memory()
		# add permanent memory saving function for EEPROM memory

	def print_memory(self) :
		print('\n-------------------- DYNAMIXEL MEMORY --------------------') 
		for address in self.memory.keys() : 
			try :
				print(hex(address) + ' --> ' + hex(self.memory[address]))
			except TypeError : 
				print(hex(address) + ' --> ' + '-')
		print('-----------------------------------------------------------')
		

# dynamixel = Dynamixel()
# dynamixel.read_memory()
# dynamixel.write('\xff\xff\x02\x07\x03\x1e')
# dynamixel.read(dynamixel.inWaiting())