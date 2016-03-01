import sys # sys.platform
import glob # glob.glob
import serial # serial.Serial  
import platform # platform.system
import inspect # inspect.stack
import time     #time.time, time.sleep

from utils import exception_handling
from utils.debug import debug
###from utils.dummy_dynamixel import dummy_dynamixel

def get_connected_arduino_objects(arduino1_flag,arduino2_flag) : 
    #returns a list [arduino_1_serial_object,arduino_2_serial_objects

    global arduino_1_obj, arduino_2_obj
    global serial_objects_list
    global dynamixel_port

    serial_objects_list = get_available_serial_objects()

    [arduino_1_obj,arduino_2_obj] = get_connected_arduino_ports(arduino1_flag,arduino2_flag)

    serial_objects_list[0].close() # CHANGE --- close all open ports
    dynamixel_port = 'com8'

    def decorate_serial_object(serial_object) : 
        
        def decorator(function) :
            def wrapper(*args,**kwargs) : 
                return_value = None
                try : 
                    return_value = function(*args,**kwargs)
                except OSError :
                    print('arduino disconnected')
                else :
                    return return_value
            return wrapper

        def set_baudrate(baudrate) : 
            try :
                serial_object.baudrate = baudrate
            except serial.serialutil.SerialException :
                print('arduino disconnected')
        
        serial_object.write = decorator(serial_object.write)
        serial_object.read = decorator(serial_object.read)
        serial_object.inWaiting = decorator(serial_object.inWaiting)
        serial_object.set_baudrate = set_baudrate
        return serial_object

    arduino1 = decorate_serial_object(arduino_1_obj)
    arduino1.set_baudrate(57600)
    arduino2 = decorate_serial_object(arduino_2_obj)
    arduino2.set_baudrate(57600)

    return [arduino1,arduino2]

def get_connected_dynamixel_object(dynamixel_module) : 
    global serial_objects_list

    def dynamixel_handshake(serial_object) : 
        # returns True if dynamixel is connected to "serial_port", else returns False
        serial_object.baudrate = 57600
        dynamixel_module.dynamixel = serial_object
        print(serial_object)
        dynamixel_module.send_and_check(1,3,25,1)
        print("okayyy")
        print(dynamixel_module.dynamixel)
        return_value = dynamixel_module.send_and_check(2,3,25,1)        #LED for motor 2
        print(return_value)

    dynamixel_handshake(serial_objects_list[0])
    print("okay")
    print("close other open ports")
    print("ok_1234")

def get_connected_arduino_ports(arduino1_flag,arduino2_flag) : 
    global serial_objects_list

    for obj in serial_objects_list:
        print(obj.port)

    def handshake(device) : 
        # returns the serial_port in "serial_ports_list" to which the "device" is connected

        def arduino_1_handshake(serial_port) :
            # returns True if arduino2 is connected to "serial_port", else returns False

            arduino = serial_port
            arduino.baudrate = 57600
            ARDUINO_NUMBER = '0'
            
            def send_and_check(instruction_packet,timeout=5) :
                arduino.write(instruction_packet) 
                start_time = time.time()
                elapsed_time = 0

                while elapsed_time < timeout :
                    elapsed_time = time.time() - start_time
                    if arduino.inWaiting() > 0 :
                        returned_data = arduino.read(arduino.inWaiting())
                        if ARDUINO_NUMBER in returned_data :
                            return True
                
                return False

            return send_and_check('h')

        def arduino_2_handshake(serial_port) : 
            # returns True if arduino1 is connedted to "serial_port", else returns False
            
            arduino = serial_port
            arduino.baudrate = 57600
            OKAY_CHARACTER = 'O'        # Okay I am doing it
            DONE_CHARACTER = 'D' 
            ARDUINO_NUMBER = '2'
            NOT_OKAY_CHARACTER = 'N'    # Not Okay
            IN_RESET_CHARACTER = 'R'
            MOVE_OUT_OF_RESET_COMMAND = 114 # "r"
            START_BYTE = 255
            
            @debug() 
            def send_and_check(instruction_packet,timeout=10) :
                arduino.write(instruction_packet) 
                start_time = time.time()
                elapsed_time = 0

                FLAG = 0
                while elapsed_time < timeout and FLAG != 2:
                    elapsed_time = time.time() - start_time
                    if arduino.inWaiting() > 0 :
                        returned_data = arduino.read(arduino.inWaiting())
                        # print(returned_data)
                        if IN_RESET_CHARACTER in returned_data :
                            send_and_check(chr(START_BYTE) + chr(MOVE_OUT_OF_RESET_COMMAND) + chr(0))   # is timeout - elapsed_time correct
                            print('writing instruction packet again')
                            arduino.write(instruction_packet)
                            FLAG = 0
                        if OKAY_CHARACTER in returned_data :
                            FLAG += 1
                        if ARDUINO_NUMBER in returned_data :
                            FLAG += 1 
                        if DONE_CHARACTER in returned_data : 
                            FLAG += 1 
                        if NOT_OKAY_CHARACTER in returned_data : 
                            arduino.write(instruction_packet)
                if FLAG == 2 :
                    return True
                return False
                # try changing this to --> return FLAG == 2

            return send_and_check(chr(255)+'h'+chr(0)) 

        device_handshake_dictionary = {
            'arduino1' : arduino_1_handshake,
            'arduino2' : arduino_2_handshake,
        }

        handshake_function = device_handshake_dictionary.get(device)

        ignore_serial_ports = ['/dev/tty.Bluetooth-Incoming-Port']

        for serial_port in serial_objects_list :
            if serial_port.port not in ignore_serial_ports :
                if handshake_function(serial_port) == True :
                    serial_objects_list.pop(serial_objects_list.index(serial_port))
                    return serial_port
        raise OSError(device + ' is not connected')

    if(arduino1_flag):
        arduino_1_obj = handshake('arduino1')
        print('arduino 1 port --> ',arduino_1_obj.port)
    else:
        # arduino_1_obj =
        pass # CHANGE
    if(arduino2_flag):
        arduino_2_obj = handshake('arduino2')
        print('arduino 2 port --> ',arduino_2_obj.port)
    else:
        # arduino_2_obj = 
        pass # CHANGE
    return [arduino_1_obj,arduino_2_obj]

def get_available_serial_objects():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            result.append(s)
        except (OSError, serial.SerialException):
            pass

    time.sleep(3)

    return result

def find_dynamixel_and_arduino() :
    global dynamixel_port,arduino1_port,arduino2_port

    #check if this function called by dynamixel.py, arduino1.py or arduino2.py
    #return the arduino1 or arduino2 or dynamixel port respectively
    stack = inspect.stack()
    if 'dynamixel' in stack[1][1] :
        try :
            dynamixel = serial.Serial(port = dynamixel_port)      #create an instance of the serial.Serial class 
        except :
            dynamixel = dummy_dynamixel.Dynamixel()
            return dynamixel
            # exception_handling.handle_exception('dynamixel','cant connect')
        else :
            print(dynamixel)
            dynamixel.baudrate = 57600                 #set baudrate equal to 57600
            return dynamixel
            # dynamixel = dummy_dynamixel.Dynamixel()
            # return dynamixel
            
    elif 'arduino1' in stack[1][1] :
        try :
            arduino1 = serial.Serial(port = arduino1_port)
        except :
            raise OSError('ARDUINO1 NOT CONNECTED')
        else :
            print(arduino1)
            arduino1.baudrate = 9600
            return arduino1

    elif 'arduino2' in stack[1][1] :
        try : 
            arduino2 = serial.Serial(port = arduino2_port)
        except : 
            raise OSError('ARDUINO2 NOT CONNECTED')
        else :
            print(arduino2)
            arduino2.baudrate = 9600
            return arduino2
    else : 
        print('serial_ports_setup.py called by some module\
            other that dynamixel.py or arduino.py')
