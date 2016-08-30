import string_handling 

text_file = ''
with open('variable2.txt','r') as f : 
	text_file = f.read()
print(text_file)

def get_variables(string) : 

	def lines_from_string(string) : 
		return_array = []
		append_string = ''

		for i in range(len(string)) :
			element = string[i] 
			if element == '\n': 
				return_array.append(append_string)
				append_string = ''
			elif i == len(string)-1:  
				append_string += element
				return_array.append(append_string)
			else : 
				append_string += element
		print(return_array)
		temp_return_array = []
		for line in return_array : 
			line = string_handling.remove_useless(line,[' ','\n','\t'])
			if(line.startswith('#')) :
				pass
			else :
				temp_return_array.append(line)
		return_array = temp_return_array
		print(return_array)
		return return_array

	def decode_range(range_) : 
		range_ = range_[1:-1].split(':')
		print(range_)
		lower_limit = 0
		upper_limit = 0
		LOWER_LIMIT = -10000
		UPPER_LIMIT = +10000 
		try :
			lower_limit = int(range_[0])
		except ValueError :
			if range_[0] == '' :
				lower_limit = LOWER_LIMIT
			else : 
				raise 'undefined range'
		try : 
			upper_limit = int(range_[1])
		except ValueError :
			if range_[1] == '' :
				upper_limit = UPPER_LIMIT 
			else : 
				raise 'undefined range'
		return [lower_limit,upper_limit]

	return_array = lines_from_string(string)

	temp_return_array = []
	for line in return_array : 
		temp_return_array.append([])
		for element in line.split(',') :
			temp_return_array[-1].append([element.split('=')[0],element.split('=')[1]]) 
	return_array = temp_return_array

	for variable_array in return_array : 
		for attribute in variable_array : 
			try :
				attribute[1] = int(attribute[1])
			except : 
				attribute[1] = decode_range(attribute[1])

	temp_return_array = []
	for variable_array in return_array : 
		temp_return_array.append(variable(variable_array))
	
	return_array = temp_return_array 	
	return return_array


class variable() : 
	def __init__(self,attribute_list) : 
		self.name = attribute_list[0][0]
		self.value = attribute_list[0][1]
		attribute_list.pop(0)
		self.attribute_dictionary = {}
		for attribute in attribute_list : 
			if attribute[0] == 'range' : 
				self.range = attribute[1]
			elif attribute[0] == 'default' :
				self.default = attribute[1]
			else :
				self.attribute_dictionary[attribute[0]] = attribute[1]

		try :
			a = self.range
		except : 
			self.range = [-10000,10000]
		else :
			pass	

	def change_value(self,value):
		if value < self.range[0] or value > self.range[1] : 
			print('eee hamse naa ho payega')
			raise OSError
		else : 
			self.value = value 

a = get_variables(text_file)
print(a)
