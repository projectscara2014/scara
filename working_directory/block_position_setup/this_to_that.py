import var
from math import*

a = var.LENGTH_OF_FIRST_ARM
b = var.LENGTH_OF_SECOND_ARM

def angles_to_coordinates(alpha,beta):
	theta = beta_to_theta(beta)
	R = a*cos(radians(theta)) + b*cos(radians(mod(beta)-theta))
	entire_list = calculate_entire_block_position_list(alpha,beta) 
	alpha_1 = entire_list[0]
	eta = alpha_1 - theta
	y = R*cos(radians(eta))
	x = R*sin(radians(eta))
	return [x,y]

def coordinates_to_angles(x,y) :
    global a
    global b

    hypotenuous = sqrt((x**2)+(y**2))
    n = degrees(atan(x/y))
    theta = degrees(acos(((a**2)+(hypotenuous**2)-(b**2))/(2*hypotenuous*a*1.0)))
    alpha = n+ theta
    beta = -1* (theta+ degrees(acos(((hypotenuous**2)+(b**2)-(a**2))/(2*hypotenuous*b*1.0))))
    # print 'hypotenuous=', hypotenuous
    # print 'n=', n
    # print 'theta=', theta
    # print 'alpha_1', alpha_1
    # print 'beta_1=', beta_1
    return [alpha,beta]

def coordinates_to_list(x,y):
	[alpha,beta] = coordinates_to_angles(x,y)
	return_block_array = calculate_entire_block_position_list(alpha,beta)
	return return_block_array

def calculate_entire_block_position_list(alpha,beta,s=False) :
	global a
	global b
	default_s_value = 45
	if not s : 
		s = default_s_value
	

	def calculate_other_values(alpha,beta,s) :
		alpha_1 = alpha_2 = beta_1 = beta_2 = s1 = s2 = z = 0

		theta = beta_to_theta(beta)

		if(beta < 0) : 
			beta_1 = beta
			alpha_1 = alpha
			s1 = s			
			alpha_2 = alpha_1 - 2*theta
			beta_2 = -beta_1

			if(alpha_2 < -var.MAXIMUM_ALPHA) : 
				'''
				checking whether calcuated angle exceeds limit
				'''
				alpha_2 = alpha_1 
				beta_2 = beta_1

			s2 = (s1 - 2*(z-theta))%90

		if(beta > 0) : 
			beta_2 = beta
			alpha_2 = alpha
			s2 = s
			alpha_1 = alpha_2 + 2*theta
			beta_1 = -beta_2

			if(alpha_1 > var.MAXIMUM_ALPHA) : 
				'''
				checking whether calcuated angle exceeds limit
				'''
				alpha_1 = alpha_2
				beta_1 = beta_2
			
			s1 = (s2 + 2*(z-theta))%90

		#print([alpha_1,beta_1,alpha_2,beta_2,s1,s2,1])
		return [alpha_1,beta_1,alpha_2,beta_2,s1,s2,1]

	return calculate_other_values(alpha,beta,s)

def beta_to_theta(beta):
	z = mod(beta)
	x = sin(radians(z))
	y = cos(radians(z))
	theta = degrees(atan(x*1.0/((a*1.0/b)+y)))
	return theta

def mod(n) : 
	if n < 0 : n *= -1
	return n

def beta_to_y(beta):
	theta = beta_to_theta(beta)
	y = a*cos(radians(theta))+b*cos(radians(mod(beta)-theta))
	return y
# def offset_angles(alpha,beta):
# 	  for i in range (n):
	  	

# print(calculate_entire_block_position_list(20,-30))
# print(coordinates_to_angles(0,20))
# print(beta_to_theta(-72))
# print(coordinates_to_list(0,20))
# print(angles_to_coordinates(72.78,-134.96))
