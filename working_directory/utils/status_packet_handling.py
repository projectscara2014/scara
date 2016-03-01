from utils import string_handling # string_handling.char_to_int
from utils import exception_handling # handle_exception

def print_packet(packet) :

    # for character in packet :
    #       print(hex(char_to_int(character)),end=' ')
    # print()

    for character in packet :
        print (hex(string_handling.char_to_int(character))),
    print

def get_status_packet(instruction_packet,status_packet) : 

	'''
    retrives status packet from the string returned by dynamixel.
    eliminates all the noise, and extra bits from the status packet
    returned by the dynamixel
    '''
    
    #------------------ comment when dynamixel 1 works ------------------------
	if(instruction_packet[2] == '\x01'):
		return True
    #-------------------------------------------------------------------------
	
	common_string = ''		# is the string of initial characters that need to
							# be both in the instruction packet and the status packet
	for i in range(3) : 
		common_string += instruction_packet[i]
	if(common_string not in status_packet) : 
		print('common string not there')
		# CHANGE -- PRINT TO GUI
		return False 
		
	#check the index of the character where the status packet actually starts.
    #basically counter the effects of noise in the received status packet
    #by finding exactly where the status packet is in the string
	for i in range(len(status_packet)):
		if status_packet[i] == common_string[0] and \
		status_packet[i+1] == common_string[1] and \
		status_packet[i+2] == common_string[2]:
			break
		# if status_packet[i,i+3] == common_string[:] :
		# 	break

	number_of_parameters = string_handling.char_to_int(status_packet[i+3]) - 2
	error_byte = status_packet[i+4]
	parameters = ''
	for j in range(i+5,i+5+number_of_parameters) : 
		parameters += status_packet[j]
	checksum = status_packet[i+5+number_of_parameters]

	return_status_packet = ''
	return_status_packet += common_string
	return_status_packet += chr(number_of_parameters + 2)
	return_status_packet += error_byte
	return_status_packet += parameters
	return_status_packet += checksum
	
	def check_checksum(status_packet) :

		def not_checksum(l) :
			checksum = 0
			for i in range(len(l)) : 
				checksum += l[i]
			not_checksum = (~checksum)&0xff
			return not_checksum

		checksum = []
		for i in range(2,len(status_packet)-1) : 
			checksum.append(string_handling.char_to_int(status_packet[i]))
		not_checksum_ = not_checksum(checksum)
	
		if(chr(not_checksum_) != status_packet[-1]) : 
			return False
		return True
		
	#finally, check if checksum is correct
	if(check_checksum(return_status_packet)) : 
		return return_status_packet
	return False

def check_for_error(status_packet) : 
	
	'''
    Checks for error in status packet.
    Returns a list containing the bit numbers that contain errors in the 
    error bit, as returned by the dynamixel.
    '''
    
	error_byte = string_handling.char_to_int(status_packet[4])
	if(error_byte == 0) : 
		return False
	else : 
		error_byte_list = []
		for i in range(8) :
			error_byte_list.append((int(error_byte/(2**i)))&0x01)
		return error_byte_list

def error_service_routine(error_byte_list,type = 0) : 

	if(type == 0) :
	
		error = {
		0 : 'INPUT VOLTAGE ERROR',
		1 : 'ANGLE LIMIT ERROR',
		2 : 'OVERHEATING ERROR',
		3 : 'RANGE ERROR',
		4 : 'CHECKSUM ERROR',
		5 : 'OVERLOAD ERROR',
		6 : 'INSTRUCTION ERROR',
		7 : 'INVALID ERROR BYTE', 
		}
		
		for i in range(len(error_byte_list)) :
			if(error_byte_list[i]) :
				exception_handling.handle_exception(__name__,error.get(i))
        # CHANGE -- DECIDE ERROR PRIORITY
        
	elif(type == 1) : 
		error_message = 'USER DEFINED ERROR : '
		error = {
		1 : 'COMMUNICATION ERROR'
		}
		error_message += error.get(error_byte_list)
		print(error_message)
		# CHANGE -- ERROR SERVICE ROUTINE

# def log(string) :
#   logs = open(logs.txt)
#   import time
#   time.
# status_packet = get_status_packet('\xff\xff\x02\x05\x03\x1e\x00\x00\xd7','\x03\x23\xff\xff\x02\x03\x03\x01\xf6\xa1\xb4')
# print_packet(status_packet)

# b = check_for_error(status_packet)
# print(b)
# error_service_routine(b)
# error_service_routine(1,type=1)