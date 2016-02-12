import os
os.chdir('C:\Users\Akash\Desktop\Scara\\block_position_setup\\rana_mark2')
# import dynamixel
# import arduino

import this_to_that

def run() : 

	def set(motor) :
		angle=0 
		if(motor == 'dynamixel') :
			angle = 'alpha'
		elif(motor == 'arduino') : 
			angle = 's'
			#motor = arduino
		else : 
			print('invalid motor name\n')
		previous = 0
		new = raw_input('enter the value of ' + str(angle) + ' or press y if happy with the value : ')
		try : 
			new = int(new) 
		except ValueError : 
			if(new == 'y') : 
				return previous
			print('INVALID INPUT VALUE, PLEASE ENTER AN INTEGER')
			return(set(motor))

		while(new is not 'y') : 
			previous = new
			#motor.write(angle)
			new = raw_input('enter the value of ' + str(angle) + ' or press y if happy with the value : ')
			try : 
				new = int(new) 
			except ValueError : 
				if(new == 'y') : 
					return previous
				print('INVALID INPUT VALUE, PLEASE ENTER AN INTEGER')
				return(set(motor))
		return int(previous)

	alpha = set('dynamixel')
	print('SWITCH OF POWER BEFORE CHANGING DYNAMIXEL POSITION')
	print
	raw_input('press enter when you have setup dynamixel 2 position, and clear away from the motor')
	#dynamixel1.write(alpha)
	yes_or_no = raw_input("if you are happy with the current position press 'y' else 'n' ? ")
	while(yes_or_no is not 'y') :
		print('SWITCH OF POWER BEFORE CHANGING DYNAMIXEL POSITION')
		print
		raw_input('press enter when you have setup dynamixel 2 position and clear away from the motor')
		#dynamixel1.write(alpha)
		yes_or_no = raw_input('are you happy with the current position ? ')
		# yes_or_no = 'y'

	#beta = dyna2.read()
	beta = 0 # remove when you uncomment the above statement
	s = set('arduino')

	entire_block_list = this_to_that.calculate_entire_block_position_list(alpha,beta,s)

	if(entire_block_list[0] is alpha) : 
		a = entire_block_list[2]
		b = entire_block_list[3]
		s_ = entire_block_list[5]
	else : 
		a = entire_block_list[0]
		b = entire_block_list[1]
		s_ = entire_block_list[4]
	#dynamixel1.write(a)
	#dynamixel2.write(b)
	#arduino.write(s)
	#arduino.pick()
	#arduino.place()
	print(entire_block_list)

	print("bhai kuch jhol hai... check later")

run()

# l = [[[],[]],[[],[],[]],[[],[],[],[]],[[],[]],[[]],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# def get_max_no_of_blocks(character) : 
# 	global l
# 	def char_to_int(character) : 
# 		for i in range(256) : 
# 			if(chr(i) == character) : 
# 				return i
# 	character = character.upper()
# 	index = char_to_int(character) - 65
# 	return len(l[index])

# print(get_max_no_of_blocks('b'))
