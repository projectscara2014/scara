class Dynamixel : 
	
	def __init__(self) : 
		self.status_packet = []

		self.instruction_packet = []
		self.motor_id = ''
		self.instruction_packet_length = ''
		self.instruction= ''
		self.parameters = []
	
	def read(self,in_waiting) : 
		return self.make_string_from_list(self.status_packet)
			
	def write(self,instruction_packet) : 
		instruction_packet = list(instruction_packet)
		self.motor_id = instruction_packet[2]
		self.instruction_packet_length = instruction_packet[3]
		self.instruction = instruction_packet[4]
		self.parameters = instruction_packet[5:-1]
		self.status_packet.extend(self.build_status_packet())
		self.build_status_packet()
		self.print_packet(self.status_packet)

	def inWaiting(self) : 
		return(len(self.status_packet))

	def build_status_packet(self) : 

		def not_checksum(l) :
			checksum = 0
			for i in range(len(l)) :
				checksum += l[i]
			not_checksum = (~checksum)&0xff
			return not_checksum
		instructions_that_return_parameters = ['\x02']
		
		status_packet = ['\xff','\xff']
		status_packet.append(self.motor_id)
		if self.instruction not in instructions_that_return_parameters : 
			status_packet.append('\x02')	#status packet length
			status_packet.append('\x00')	#error byte

		else :
			#instruction returns parameters --> read
			pass

		checksum = [ord(self.motor_id),2]
		for parameter in self.parameters : 
			checksum.append(ord(parameter))

		status_packet.append(chr(not_checksum(checksum)))
		return status_packet

	def print_packet(self,packet) :
		packet = self.make_string_from_list(packet)	
		for character in packet :
			print(hex(ord(character)),end='/')
		print()

	def make_string_from_list(self,list_) : 
		return_string = ''
		for element in list_ : 
			return_string += str(element) 
		return return_string
		
dynamixel = Dynamixel()
dynamixel.write('\xff\xff\x02\x07\x03\x1e')
dynamixel.read(dynamixel.inWaiting())