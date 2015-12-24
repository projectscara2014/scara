import sys # sys.platform
import glob # glob.glob
import serial # serial.Serial  
import platform # platform.system
import inspect # inspect.stack

def find_dynamixel_and_arduino() :

    def serial_ports():
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
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    serial_ports_list = serial_ports()
    
    system = platform.system()
    print('system --> ',system)
    print('available serial ports : ',serial_ports_list)
    dynamixel = ''
    arduino = ''

    #for unix
    if system.startswith('Darwin') :
        for port in serial_ports_list :
            if port.startswith('/dev/tty.usbserial') :
                dynamixel = port
            elif port.startswith('/dev/tty.usbmodem') :
                arduino = port
    #for windows
    elif system.startswith('Win') :
        if len(serial_ports_list) != 2 :
            print("Connect Exactly two serial devices")
        dynamixel = 'com8'
        arduino = 'com3'
    #for others
    else :
        print('unsupported operating system')

    #check if this function called by dynamixel.py or arduino.py
    #return the arduino or arduino or dynamixel port respectively
    stack = inspect.stack()
    # print('checking stack') #comment after testing
    if 'dynamixel' in stack[1][1] :
        return[dynamixel]
    elif 'arduino' in stack[1][1] :
        return[arduino]


__all__ = ['find_dynamixel_and_arduino']

