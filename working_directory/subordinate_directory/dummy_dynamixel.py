class dynamixel : 
	
	def __init__(self) : 
		self.motor_id
	
	def read(self,in_waiting) : 
		return self.status_packet
	
	def write(self,instruction_packet) : 
		instruction_packet = list(instruction_packet)
		self.motor_id = instruction_packet[2]
		self.instruction_packet_length = instruction_packet[3]
		self.instruction = instruction_packet[4]
		self.parameters = instruction_packet[5:-1]
		self.status_packet = self.build_status_packet()

		
	def build_status_packet(self) : 
		def not_checksum(l) :
			checksum = 0
			for i in range(len(l)) :
				checksum += l[i]
			not_checksum = (~checksum)&0xff
			return not_checksum

        instructions_that_return_parameters = ['\x02']

        status_packet = '\xff\xff'
        status_packet += self.motor_id
       
        if self.instruction not in instructions_that_return_parameters : 
        	status_packet += '\x02'	#status packet length
        	status_packet += '\x00'	#error byte
        	checksum = [self.motor_id,2]
        	status_packet.append(not_checksum(checksum))
        else : 
        	pass

       	
	    return status_packet 

        # instructions_that_require_parameters = [0x02,0x03,0x04]
        # instruction_length_ = instruction_length(instruction,*args)
        # checksum = [motor_id,instruction_length_,instruction]
        # if(instruction in instructions_that_require_parameters) :
        #     for i in range(len(args)) :
        #         checksum.append(args[i])
        # not_checksum_ = not_checksum(checksum)
        # instruction_packet = '\xff\xff'
        # for i in range(len(checksum)) :
        #     instruction_packet += chr(checksum[i])
        # instruction_packet += chr(not_checksum_)
        # #print (list(instruction_packet))
        # return(instruction_packet)
