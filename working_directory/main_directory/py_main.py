###from main_directory import lookup
from subordinate_directory import serial_ports_setup

[arduino1_serial_object,arduino2_serial_object] = serial_ports_setup.get_connected_arduino_objects()
print(arduino1_serial_object)
print(arduino2_serial_object)
from main_directory import arduino1
arduino1.init(arduino1_serial_object)
arduino1.dynamixel_initialization1()

# dynamixel_serial_object = serial_ports_setup.get_connected_dynamixel_object(dynamixel)
from main_directory import dynamixel
arduino1.dynamixel_initialization2()
# import sys
# sys.exit(0)

from main_directory import arduino2
arduino2.init(arduino2_serial_object)


import sys
sys.exit(0)

from main_directory import lookup

import time

from subordinate_directory.debug import debug

CURRENT_ARRAY_LENGTH = 0
CURRENT_ARRAY = []
DISPLAY_AREA_POSITIONS = []

DISPLAY_AREA_TEMP = [[[346, -699, -347, 699, 45, 50.35959481963653, 1]], [[291, -693, -395, 693, 45, 50.30605210551902, 1], [395, -693, -291, 693, 45, 50.30605210551902, 1]], [[229, -671, -436, 671, 45, 50.14344516933812, 1], [346, -699, -347, 699, 45, 50.35959481963653, 1], [435, -671, -230, 671, 45, 50.14344516933812, 1]], [[161, -635, -468, 635, 45, 49.86503213862371, 1], [291, -693, -395, 693, 45, 50.30605210551902, 1], [395, -693, -291, 693, 45, 50.30605210551902, 1], [467, -635, -161, 635, 45, 49.86503213862371, 1]], [[86, -582, -490, 582, 45, 49.45627639295879, 1], [229, -671, -436, 671, 45, 50.14344516933812, 1], [346, -699, -347, 699, 45, 50.35959481963653, 1], [435, -671, -230, 671, 45, 50.14344516933812, 1], [489, -582, -87, 582, 45, 49.45627639295879, 1]]]

FLAG = False

@debug()
def modify_blocks(obj):
    global CURRENT_ARRAY_LENGTH
    global CURRENT_ARRAY
    global DISPLAY_AREA_POSITIONS
    global FLAG

    CURRENT_ARRAY_LENGTH = len(CURRENT_ARRAY)
    global_string = ''
    string = CURRENT_ARRAY
    FLAG = False

    display_area_calc()

    print(CURRENT_ARRAY_LENGTH)
    print("-----------------")
    for i in range (CURRENT_ARRAY_LENGTH):
        if(CURRENT_ARRAY[i] == " "):
            global_string+=" "
            continue
        print(i)
        # print("LOOKUP_OUTPUT = ",lookup.LOOKUP_OUTPUT)
        # print("DYNA_1_POS = ",lookup.DYNA_1_POS)
        # print("DYNA_2_POS = ",lookup.DYNA_2_POS)
        #--------------- PICK FORWARD --------------------------
        print("Picking ",CURRENT_ARRAY[i]," from arena")
        
        global_string+=string[i]
        obj.update_label(global_string)

        lookup.lookup(CURRENT_ARRAY[i],0)
        # # eg:- "A",pick
        # print("LOOKUP_OUTPUT = ",lookup.LOOKUP_OUTPUT)
        dynamixel.GO_TO_DYNA_1_POS = lookup.LOOKUP_OUTPUT[0]
        dynamixel.GO_TO_DYNA_2_POS = lookup.LOOKUP_OUTPUT[1]
        dynamixel.dyna_move()
        lookup.DYNA_1_POS = dynamixel.GO_TO_DYNA_1_POS
        lookup.DYNA_2_POS = dynamixel.GO_TO_DYNA_2_POS
        #arduino.pick(LOOKUP_OUTPUT[2])
        
        # print("DYNA_1_POS = ",lookup.DYNA_1_POS)
        # print("DYNA_2_POS = ",lookup.DYNA_2_POS)
        # print("----")
        #-------------------------------------------------------
        time.sleep(3)
        print("----")
        #---------------- PLACE FORWARD ------------------------
        print("Placing ",CURRENT_ARRAY[i]," on display area")

        global_string+='....'
        obj.update_label(global_string)

        dynamixel.GO_TO_DYNA_1_POS = DISPLAY_AREA_POSITIONS[i][0]
        dynamixel.GO_TO_DYNA_2_POS = DISPLAY_AREA_POSITIONS[i][1]
        dynamixel.dyna_move()
        lookup.DYNA_1_POS = dynamixel.GO_TO_DYNA_1_POS
        lookup.DYNA_2_POS = dynamixel.GO_TO_DYNA_2_POS
        #arduino.place(DISPLAY_AREA_something)
        p = i+1
        if(FLAG):
            break
        #-------------------------------------------------------
        print("-----------------")
        time.sleep(3)
    print("wait thoda...\nwait thoda...\nwait thoda...")
    print("-----------------")
    for k in range (p):
        i = p-k-1
        if(CURRENT_ARRAY[i] == " "):
        	global_string = global_string[:-1]
        	continue
        #----------------- PICK REVERSE ------------------------
        print("Picking ",CURRENT_ARRAY[i]," from display area")

        global_string = global_string[:-4]
        obj.update_label(global_string)

        dynamixel.GO_TO_DYNA_1_POS = DISPLAY_AREA_POSITIONS[i][0]
        dynamixel.GO_TO_DYNA_2_POS = DISPLAY_AREA_POSITIONS[i][1]
        dynamixel.dyna_move()
        lookup.DYNA_1_POS = dynamixel.GO_TO_DYNA_1_POS
        lookup.DYNA_2_POS = dynamixel.GO_TO_DYNA_2_POS
        #arduino.pick(DISPLAY_AREA_something)
        
        #-------------------------------------------------------
        time.sleep(3)
        print("----")
        #--------------- PLACE REVERSE --------------------------
        print("Placing ",CURRENT_ARRAY[i]," in arena")

        global_string = global_string[:-1]
        obj.update_label(global_string)

        lookup.lookup(CURRENT_ARRAY[i],1)
        dynamixel.GO_TO_DYNA_1_POS = lookup.LOOKUP_OUTPUT[0]
        dynamixel.GO_TO_DYNA_2_POS = lookup.LOOKUP_OUTPUT[1]
        dynamixel.dyna_move()
        lookup.DYNA_1_POS = dynamixel.GO_TO_DYNA_1_POS
        lookup.DYNA_2_POS = dynamixel.GO_TO_DYNA_2_POS
        #arduino.place(LOOKUP_OUTPUT[2])
        
        #-------------------------------------------------------
        print("-----------------")
        time.sleep(3)
	print("bring it on")

@debug()
def display_area_calc():
    global CURRENT_ARRAY_LENGTH
    global DISPLAY_AREA_POSITIONS
    global CURRENT_ARRAY_LENGTH
    global DISPLAY_AREA_TEMP

    DISPLAY_AREA_POSITIONS = DISPLAY_AREA_TEMP[CURRENT_ARRAY_LENGTH -1]

def check_if_blocks_out_of_place():
    f=0

# dynamixel.move_to(400,1500)