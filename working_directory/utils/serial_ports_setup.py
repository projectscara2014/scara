import sys # sys.platform
import glob # glob.glob
import serial # serial.Serial  
import platform # platform.system
import inspect # inspect.stack
import time     #time.time, time.sleep

from utils.exception_handling import handle_exception
from utils.debug import debug
#### from utils.dummy_dynamixel import dummy_dynamixel

def get_connected_arduino_objects(arduino1_flag,arduino2_flag) : 
    #returns a list [arduino_1_serial_object,arduino_2_serial_objects

    global arduino_1_obj, arduino_2_obj
    global serial_objects_list

    serial_objects_list = get_available_serial_objects()

    [arduino_1_obj,arduino_2_obj] = get_connected_arduino_ports(arduino1_flag,arduino2_flag)

    # serial_objects_list[0].close() # CHANGE --- close all open ports

    def decorate_serial_object(serial_object) : 
        
        def decorator(function) :
            def wrapper(*args,**kwargs) : 
                return_value = None
                try : 
                    return_value = function(*args,**kwargs)
                except OSError, serial.serialutil.SerialException :
                    handle_exception("disconnected") #CHANGE
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

def get_connected_arduino_ports(arduino1_flag,arduino2_flag) : 
    '''
    Tries to perform handshaking with each connected device and determines the port numbers for connected Arduino devices
    Returns respective Serial Objects
    '''
    global serial_objects_list

    for obj in serial_objects_list:
        print(obj.port)

    def handshake(device) : 
        # returns the serial_port in "serial_ports_list" to which the "device" is connected

        def arduino_1_handshake(serial_obj) :
            # returns True if arduino2 is connected to "serial_obj", else returns False

            arduino = serial_obj
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

        def arduino_2_handshake(serial_obj):
            from comm import arduino2

            arduino2.arduino = serial_obj

            return arduino2.handshake()


        def arduino_2_handshake_old(serial_port) : 
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

        for serial_obj in serial_objects_list :
            if serial_obj.port not in ignore_serial_ports :
                print("Checking =====> " + serial_obj.port)
                if handshake_function(serial_obj) == True :
                    serial_objects_list.pop(serial_objects_list.index(serial_obj))
                    return serial_obj
        handle_exception(device+"_not_connected")

    if(arduino1_flag):
        arduino_1_obj = handshake('arduino1')
        print('arduino 1 port --> ',arduino_1_obj.port)
    else:
        # arduino_1_obj = DUMMY OBJECT
        pass # CHANGE
    if(arduino2_flag):
        # arduino_2_obj = arduino_1_obj ### UNCHANGED 16/6/16
        arduino_2_obj = handshake('arduino2')
        print('arduino 2 port --> ',arduino_2_obj.port)
    else:
        # arduino_2_obj = DUMMY OBJECT
        pass # CHANGE
    return [arduino_1_obj,arduino_2_obj]

def get_available_serial_objects():
    """Lists connected serial objects

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial objects
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

def get_connected_dynamixel_object(set_dyna_obj,send_and_check_fn) : 
    '''
    Returns the Serial object for connected "USB to RS485" module
    '''
    global serial_objects_list     # all remaining serial objects are open here

    ### CHANGE --- REMOVE THIS LATER

    # dynamixel_port = 'com5'  # CHANGE ---- WTF?

    # print(dynamixel_port)

    # try :
    #     for serial_object in serial_objects_list:
    #         print "Closing Port : " + str(serial_object.port)
    #         serial_object.close()
    #     dynamixel = serial.Serial(port = dynamixel_port)      #create an instance of the serial.Serial class 
    # except :
    #     # dynamixel = dummy_dynamixel.Dynamixel() ## UNCHANGED 16/6/16
    #     # # return dynamixel ##CHANGED 16/6/16
    #     # dynamixel = serial.Serial(port = dynamixel_port)
    #     raise RuntimeError("Dynamixel not connected") # CHANGE
    #     # exception_handling.handle_exception('dynamixel','cant connect') 
    # else :
    #     print(dynamixel)
    #     dynamixel.baudrate = 57600                 #set baudrate equal to 57600
    #     return dynamixel
    #     # dynamixel = dummy_dynamixel.Dynamixel()
    #     # return dynamixel

    ###  IF THIS WORKS THEN REMOVE UPAR KA

    # dynamixel_module = inspect.stack()[1][0]    # dynamixel module for functional usage

    def dynamixel_handshake(serial_object) : 
        '''
        returns True if dynamixel is connected to "serial_port", else returns False
        '''
        serial_object.baudrate = 57600
        # dynamixel_module.dynamixel = serial_object
        set_dyna_obj(serial_object)
        print(serial_object)

        return_value = send_and_check_fn(2,3,25,1)   #LED for motor 2
        # return_value = dynamixel_module.send_and_check(2,3,25,1)   #LED for motor 2

        print(return_value)
        return return_value

    return_object = None

    for serial_object in serial_objects_list:
        if(dynamixel_handshake(serial_object)):
            return_object = serial_object
        else:
            serial_object.close()

    if(return_object == None):
        pass
        handle_exception("dynamixel_not_connected")
    else:
        return return_object