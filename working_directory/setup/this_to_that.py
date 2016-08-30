import var
from math import*

a = var.LENGTH_OF_FIRST_ARM
b = var.LENGTH_OF_SECOND_ARM
c = var.GRIPPER_OFFSET_LENGTH
d = (b**2 + c**2)**0.5
rho = degrees(atan(c*1.0/b))

def degrees_to_coordinates(alpha,beta):
	theta = beta_to_theta(beta)
	R = a*cos(radians(theta)) + b*cos(radians(mod(beta)-theta))
	entire_list = calculate_entire_block_position_list(alpha,beta) 
	alpha_1 = entire_list[0]
	eta = alpha_1 - theta
	y = R*cos(radians(eta))
	x = R*sin(radians(eta))
	return [x,y]

def coordinates_to_degrees(x,y) :
    global a
    global b

    hypotenuous = sqrt((x**2)+(y**2))
    n = degrees(atan(x*1.0/y))
    theta = degrees(acos(((a**2)+(hypotenuous**2)-(b**2))*1.0/(2*hypotenuous*a*1.0)))
    alpha = n+ theta
    beta = -1* (theta+ degrees(acos(((hypotenuous**2)+(b**2)-(a**2))*1.0/(2*hypotenuous*b*1.0))))

    return [alpha,beta]

def coordinates_to_list(x,y):
	[alpha,beta] = coordinates_to_degrees(x,y)
	return_block_array = calculate_entire_block_position_list(degrees_to_scars(alpha),degrees_to_scars(beta))
	return return_block_array

def calculate_entire_block_position_list(alpha,beta,s) :
	# return [alpha,beta,alpha,beta,s,s,1] #comment LATER
	def calculate_other_values(alpha,beta,s) :
		# alpha, beta, s, rho are in degrees
		global a, b, c, d, rho
		# alpha_1 = alpha_2 = beta_1 = beta_2 = s1 = s2 = z = 0

		if(beta < 0): 
			beta_1 = beta
			alpha_1 = alpha
			s1 = s

			psi = -beta - rho
			beta_2 = psi - rho

			theta = calculate_theta(a,d,psi)
			alpha_2 = alpha_1 - 2*theta

			if(degrees_to_scars(alpha_2) < -var.MAXIMUM_ALPHA or degrees_to_scars(beta_2) < -var.MAXIMUM_BETA): 
				alpha_2 = alpha_1 
				beta_2 = beta_1

			eta = calculate_eta(a,d,theta)
			s2 = (180 - (s + 2*eta))%45 # CHANGE

		if(beta > 0): 
			beta_2 = beta
			alpha_2 = alpha
			s2 = s

			psi = beta + rho
			beta_1 = -(psi + rho)
			
			theta = calculate_theta(a,d,psi)
			alpha_1 = alpha_2 + 2*theta

			if(degrees_to_scars(alpha_1) > var.MAXIMUM_ALPHA or degrees_to_scars(beta_1) > var.MAXIMUM_BETA): 
				alpha_1 = alpha_2
				beta_1 = beta_2
			
			eta = calculate_eta(a,d,theta)
			s1 = (180 - (s + 2*eta))%90 # CHANGE

		return [alpha_1,beta_1,alpha_2,beta_2,s1,s2,1]

	alpha = scars_to_degrees(alpha)
	beta = scars_to_degrees(beta)

	return_array = calculate_other_values(alpha,beta,s)
	r = []
	for i in range(4) :
		r.append(int(degrees_to_scars(return_array[i])))
	for i in range(4,7) :
		r.append(int(return_array[i]))
	return r

def mod(n) : 
	if n < 0 :
		n *= -1
	return n

def scars_to_degrees(scars) :
	return scars*360.0/4096

def degrees_to_scars(angle) :
	return angle*4096.0/360

# ----- OTHER FUNCTIONS ------

def calculate_theta(arm1_length,arm2_length,arm2_angle):
	z = mod(arm2_angle)
	x = sin(radians(z))
	y = cos(radians(z))
	theta = degrees(atan(x*1.0/((arm1_length*1.0/arm2_length)+y)))
	return theta

def calculate_eta(arm1_length,arm2_length,theta):
	eta = degrees(asin(sin(radians(theta))*arm1_length*1.0/arm2_length))
	return eta

def beta_to_y(beta):
	theta = beta_to_theta(beta)
	y = a*cos(radians(theta))+b*cos(radians(mod(beta)-theta))
	return y

# print(scars_to_degrees(1500))
# print(calculate_entire_block_position_list(-200,-500,30))
# print(coordinates_to_degrees(0,20))
# print(beta_to_theta(-72))
# print(coordinates_to_list(0,20))
# print(angles_to_coordinates(72.78,-134.96))
