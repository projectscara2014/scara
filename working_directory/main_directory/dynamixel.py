# from debug import debug

import time                              #import time liabrary to use the time.sleep() function to generate delays
import serial                            #import the serial library 

from subordinate_directory import status_packet_handling
from subordinate_directory.string_handling import char_to_int

##---IMPORTANT GLOBAL VARIABLES---
GO_TO_DYNA_1_POS=0
GO_TO_DYNA_2_POS=0

##---INITIALIZATION VARIABLES---
dynamixel = ''

#---DYNAMIXEL VARIABLES---
motor_1_offset = 2048 - 15
motor_2_offset = 2048 + 50

##---LIMITING VARIABLES---
send_and_check_limit = 10
dyna_write_limit     = 3 
read_limit           = 80
stall_count_limit    = 10
max_acceptable_error_in_position = 0

# def init() : 
#     global dynamixel
#     dynamixel = serial_ports_setup.find_dynamixel_and_arduino()
#     try :
#         dynamixel.print_memory()
#     except :
#         pass
#     dynamixel_initializations()

def dynamixel_initializations():
    send_and_check(1,3,26,8,8,24)   #PID for motor 1
    send_and_check(2,3,26,8,8,24)   #PID for motor 2
    send_and_check(1,3,32,0,1)      #SPEED for motor 1
    send_and_check(2,3,32,0,1)      #SPEED for motor 2
    send_and_check(1,3,25,1)        #LED for motor 1
    send_and_check(2,3,25,1)        #LED for motor 2

def send_and_check(motor_id,instruction,*args) :
    '''
    Ensures the packet has been succesfully delivered
    '''
    def build_instruction_packet(motor_id,instruction,*args) : 
        
        def not_checksum(l) :
            checksum = 0
            for i in range(len(l)) :
                checksum += l[i]
            not_checksum = (~checksum)&0xff
            return not_checksum

        def instruction_length(instruction,*args) :
            instructions_that_require_parameters = [0x02,0x03,0x04]
            if(instruction in instructions_that_require_parameters) :
                return (len(args) + 2)
            else :
                return 2

        instructions_that_require_parameters = [0x02,0x03,0x04]
        instruction_length_ = instruction_length(instruction,*args)
        checksum = [motor_id,instruction_length_,instruction]
        if(instruction in instructions_that_require_parameters) :
            for i in range(len(args)) :
                checksum.append(args[i])
        not_checksum_ = not_checksum(checksum)
        instruction_packet = '\xff\xff'
        for i in range(len(checksum)) :
            instruction_packet += chr(checksum[i])
        instruction_packet += chr(not_checksum_)
        #print (list(instruction_packet))
        return(instruction_packet)

    instruction_packet = build_instruction_packet(motor_id,instruction,*args)
    
    global send_and_check_limit
    count = 0

    while(count < send_and_check_limit) :
        #print("instruction packet =>",list(instruction_packet))
        dynamixel.write(instruction_packet)
        time.sleep(0.05)
        status_packet = dynamixel.read(dynamixel.inWaiting())
        #print("raw status",list(status_packet))
        status_packet = status_packet_handling.get_status_packet(instruction_packet,status_packet)
        print(status_packet)
        if(status_packet == False) :
            # No status packet / Incorrect status packet
            count+=1
        elif(status_packet == True):
            print("hi")
            # TRUE ONLY WHEN Dynamixel 1
            return True
        else:
          #  print("decoded status",list(status_packet))
            error = status_packet_handling.check_for_error(status_packet)
            if(error == False):
                return status_packet
            else:
                status_packet_handling.error_service_routine(error)
    print("send_and_check>>limit overshoot")
    status_packet_handling.error_service_routine(1,type=1)
    # USER DEFINED ERROR: 1 :- IN CASE OF COMMUNICATION ERROR
    return False

# FUNCTION TO MOVE THE ARM TO THE REQUIRED POSITION
def dyna_move():
    global GO_TO_DYNA_1_POS
    global GO_TO_DYNA_2_POS

    global dyna_write_limit
    count = 0

    # FUNCTION TO CORRECTLY MOVE THE DYNAMIXEL TO THE REQUIRED POSITION
    def position_write(motor_id,goal_pos) :
        global motor_1_offset
        global motor_2_offset

        if(motor_id==1):
            offset = motor_1_offset
        elif(motor_id==2):
            offset = motor_2_offset

        # FUNCTION TO CONVERT ANGLES TO POSITIONS
        def angle_to_hex(angle,offset):
            angle = -angle
            angle = angle + offset
            angle = angle%4096
            return [(int(angle%256)),(int(angle/256))]

        [h_byte,l_byte] = angle_to_hex(goal_pos,offset)
        #print("writing motor ",motor_id," to :-",[h_byte,l_byte])
        send_and_check(motor_id,3,30,h_byte,l_byte)

    while(count < dyna_write_limit) :
     #   print("writing to dyna")#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        position_write(1,GO_TO_DYNA_1_POS)#--------------------------->>>
        position_write(2,GO_TO_DYNA_2_POS)
      #  print("starting read procedure_______________")
        reached = till_dyna_reached()
        if(reached == True):
            break
        elif(reached == "again"):
            count +=1
        else:
            count +=1
            print("Somethings Wrong")
            print("Writing to dynamixel again")
    if(count==dyna_write_limit):
        print("dyna write limit reached")
        # CHANGE -- Handle Exception

def till_dyna_reached() :
    global GO_TO_DYNA_1_POS
    global GO_TO_DYNA_2_POS

    global read_limit
    global stall_count_limit

    def position_read():

        def angle_from_status_packet(packet,offset) : 

            def hex_to_angle(position_low,position_high,offset):
                angle = (char_to_int(position_high))*256 + char_to_int(position_low)
                angle = -angle
                angle += offset
                angle = angle%4096
                return int(angle)

            #print(list(packet))  # debug    
            number_of_parameters = char_to_int(packet[3]) - 2
            parameters = []
            for i in range(5,5+number_of_parameters) : 
                parameters.append(packet[i])
            #print("hex = ",parameters) # debug
            return hex_to_angle(parameters[0],parameters[1],offset)

        global motor_1_offset
        global motor_2_offset

        #status_packet1 = send_and_check(1,2,36,2)# UNCOMMENT when Dynamixel 1 works
        status_packet1 = "\xff\xff\x01\x04\x00\x00\x00\xfa" # COMMENT when Dynamixel 1 works
        status_packet2 = send_and_check(2,2,36,2)

        if(not(status_packet1 and status_packet2)):
            print("position_read did not get a status_packet")
            return False
        
        current_angles = [angle_from_status_packet(status_packet1,motor_1_offset)\
        ,angle_from_status_packet(status_packet2,motor_2_offset)]
        return current_angles

    count = 0
    stall_count = 0
    reqd_pos = [GO_TO_DYNA_1_POS%4096,GO_TO_DYNA_2_POS%4096]
    current_pos = position_read()
    last_pos = current_pos

    def compare(current,reqd):
        global max_acceptable_error_in_position

        current[0] = reqd[0]     # COMMENT when dynamixel 1 works
        l = zip(current,reqd)
        def mod(s):
            if(s<0):s*=-1
            return s
        
        for element in l:
            if(mod(element[0]-element[1])> max_acceptable_error_in_position):
                return False
        return True
    
    while(count < read_limit):
        if(compare(current_pos,reqd_pos)):
            return True
        elif(current_pos == last_pos):
            if(stall_count < stall_count_limit) :
                stall_count += 1
            else:
                return "again"
        else:
            stall_count = 0
            last_pos = current_pos
        current_pos = position_read()
        count +=1
    return False

#-------------------------------------------------------------------

HYPER_LIST = []

def forloop():
    pid(48,8,8)
    for i in range(0,4096):
        print("=========================="+str(i)+"=============================")
        move_to(i)
        
def store_in_list(angle):
    global HYPER_LIST

    HYPER_LIST.append(angle)

def pid(p,i,d):
    send_and_check(2,3,26,d,i,p)

def speed_control():
    speed_high = 7
    speed_low  = 0
    send_and_check(2,3,32,speed_low,speed_high)


    #k()#~~~~~~~~~~~~~~~~~!!!!!!!!@@@@@@@@@@#########!!!!!!!!!!!!!!

##pid(0,6,45)

##forloop()
##
##print(HYPER_LIST)

##k=[]
##for i in range(512):
##  if(i not in HYPER_LIST):
##      k.append(i)
##print(k)      

##def move_to(angle):
##    global GO_TO_DYNA_2_POS
##    
##    GO_TO_DYNA_2_POS = angle
##    dyna_move()

##def move_to(angle2,angle1=False):
##    global GO_TO_DYNA_1_POS
##    global GO_TO_DYNA_2_POS
##
##    if not angle1:GO_TO_DYNA_1_POS = angle1
##    GO_TO_DYNA_2_POS = angle2
##    dyna_move()

def move_to(angle1,angle2):
    global GO_TO_DYNA_1_POS
    global GO_TO_DYNA_2_POS
    GO_TO_DYNA_1_POS = (angle1)
    GO_TO_DYNA_2_POS = (angle2)
##    GO_TO_DYNA_1_POS = a(angle1)
##    GO_TO_DYNA_2_POS = a(angle2)
    dyna_move()

def send(motor_id,instruction,*args) :
    instruction_packet = build_instruction_packet(motor_id,instruction,*args)
    dynamixel.write(instruction_packet)
    time.sleep(0.05)
    status_packet = dynamixel.read(dynamixel.inWaiting())
    print("raw status",list(status_packet))

def s(i,*args):
    send(1,3,i,*args)

RANDOM_LIST_2 = []

def k(a):
    global RANDOM_LIST
    global RANDOM_LIST_2

    RANDOM_LIST = []
    
    pid(48,8,8)
    move_to(a)
    f = [y for x,y in RANDOM_LIST]
    RANDOM_LIST_2.append(f)

def a(num):
    a = int(num*4096.0/360)
    return a

#------------------------------------------------------------

'''to communicate with the dynamixel motor via the max485 ic , we need to set up a
    virtual com port and create an instance of the serial.Serial class , so as to
    use it to read data from and write data to the dynamixel
        serial<id,open=(true/false)>(port = ?,baudrate = ?,bytesize = ?,parity = 'Y/N',
    stopbits = ?,timeout = ?,xonxoff = (True/False),rtscts = (True/False),dsrdtr =
    (True/False))
'''


'''
I N S T R U C T I O N   P A C K E T :

the instruction packet for the dynamixel consists of 6 parts :
    part1) initialization :
        you need to tell the dynamixel that you are sending it an instruction packet
        for this , you need to send '0xFF' two times
        
    part2) id of the motor :
        you need to specify the id of the motor in case that more than one motors are
        connected in daisy chain configuration .
        in our case, the two motors that we are using have id's 0x01 and 0x02
        but in general there can be maximum of 254 motors connected in daisy chain
        
    part3) length of the packet :
        it is calculated as the number of parameters + 2
        
    part4)instruction :
        this is the opcode of the instruction (in hexadecimal ofcourse)
        the following are the instructions that can be used with the dynamixel motors :
            instruction 1 :
                PING (0x01) --> NO EXECUTION , IT IS USED WHEN THE CONTROLLER IS READY TO
                RECIEVE THE STATUS PACKAGE
                NUMBER OF PARAMETERS --> 0
            instruction 2 :
                READ_DATA (0x02) --> THIS COMMAND READS DATA FROM THE DYNAMIXEL
                NUMBER OF PARAMETERS --> 2
                    PARAMETER1 ---> START ADDRESS OF DATA TO BE READ
                    PARAMETER2 --> LENGTH OF DATA TO BE READ (IN BYTES) 
            instruction 3 :
                WRITE_DATA(0x03) --> THIS COMMAND WRITES DATA TO DYNAMIXEL
                NUMBER OF PARAMETERS --> 2 OR MORE
                    PARAMETER1 --> START ADDRESS TO WRITE DATA
                    PARAMETE2 --> FIRST DATA TO WRITE
                    PARAMETER3 --> SECOND DATA TO WRITE
                    ...
                    PARAMETERN --> NTH DATA TO WRITE
            instruction 4 :
                REG WRITE (0x04) --> THIS COMMAND IS SIMILAR TO WRITE DATA BUT IT REMAINS
                                     IN THE STANDBY STATE WITHOUT BEING EXECUTED UNTIL
                                     THE ACTION COMMAND IS RECEIVED
                NUMBER OF PARAMETERS --> 2 OR MORE
                    PARAMETER1 --> START ADDRESS TO WRITE DATA
                    PARAMETER2 --> FIRST DATA TO WRITE
                    PARAMETER3 --> SECOND DATA TO WRITE
                    ...
                    PARAMETERN --> NTH DATA TO WRITE
            instruction 5 :
                ACTION (0x05) --> THIS COMMAND INITIATES THE MOTIONS REGISTERED WITH THE
                                  REG WRITE INSTRUCTION
                NUMBER OF PARAMETERS --> 0
            instruction 6 :
                RESET (0x06) --> THIS COMMAND RESTORES THE STATE OF DYNAMIXEL TO FACTORY
                                 SETTINGS
                NUMBER OF PARAMETERS --> 0
            instruction 7 :
                SYNC WRITE (0x83) --> THIS COMMAND IS USED TO CONTROL SEVERAL DYNAMIXELS
                                      AT A TIME
                NUMBER OF PARAMETERS --> 4 OR MORE
                    PARAMETER1 --> START ADDRESS OF DATA TO WRITE
                    PARAMETER2 --> LENGTH OF DATA TO WRITE
                    PARAMETER3 --> FIRST ID
                    PARAMETER4 --> FIRST DATA OF FIRST ID
                    PARAMETER5 --> SECOND DATA OF FIRST ID
                    ...
                    PARAMETERX --> SECOND ID
                    PRAMETERX+1 --> FIRST DATA OF SECOND ID
                    ...
                (IN THE SYNC WRITE INSTRUCTION , THE LENGTH OF THE INSTRUCTION SHOULD
                 NOT EXCEED 143 BYTES , SINCE THE VOLUME OF THE RECEIVING BUFFER IS 143
                 BYTES )
                
    part5)parameters :
        parameter is used when the instruction requires ancillary data

    part6)check sum :
        it is used to check if the packate is damaged using commumication . checksum is
        calculated according to the formula :
            checksum = ~(id + length + instruction + parameter1 + parameter2 + .. + parameterN)
'''

'''

S T A T U S    P A C K E T :

the dynamixel executes command received from the main controller and returns the result
    to the main controller . the returned data is called the status packet .
    the status packet containg of 6 parts :

    part1)identification :
        this signal identifies the beginning of the status packet (0xFF two times)

    part2)id :
        id of the dynamixel motor which transfers the status packet

    part3)length :
        it is the length of the status packet
        it is given as number of parameters + 2

    part4)error byte :
        it displays the error status occured during the operation of the dynamixel
        each bit in the error byte has a meaning and is explained below
            BIT0 INPUT VOLTAGE ERROR --> WHEN THE APPLIED VOLTAGE IS OUT OF RANGE OF
                                         OPERATING VOLTAGE SET IN THE CONTROL TABEL
                                         IT IS SET AS 1
            BIT1 ANGLE LIMIT ERROR --> WHEN THE GOAL POSITION IS WRITTEN OUT OF THE RANGE
                                       FROM THE CW ANGLE LIMIT TO CCW ANGLE LIMIT , IT IS
                                       SET TO 1
            BIT2 OVERHEATING ERROR --> WHEN THE INTERNAL TEMPERATURE OF THE DYNAMIXEL IS
                                       OUT OF RANGE OF THE OPERATING TEMPERATURE SET IN
                                       THE CONTROL TABEL , IT IS SET AS 1
            BIT3 RANGE ERROR --> WHEN A COMMAND IS OUT OF THE RANGE FOR USE , IT IS SET AS 1
            BIT4 CHECKSUM ERROR --> WHEN THE CHECKSUM OF THE TRANSMITTED INSTRUCTION PACKET
                                    IS INCORRECT , IT IS SET AS 1
            BIT5 OVERLOAD ERROR --> WHEN THE CURRENT LOAD CAN NOT BE CONTROLLED BY THE SET
                                    TORQUE , IT IS SET AS 1
            BIT6 INSTRUCTION ERROR --> IN CASE OF SENDING AN UNDEFINED INSTRUCTION OR DELIVERING
                                       THE ACTION COMMAND WITHOUT THE REG_WRITE COMMAND , IT
                                       IS SET AS 1
            BIT7 --> 0

    part5)parameter :
        it is the data except the error
        
    part6)checksum :
        it is used to check if the packet is damaged during communication
        checksum = ~(id + length + error + parameter1 + parameter2 + ...)
--------------------------------------------------------------------------------------
'''
