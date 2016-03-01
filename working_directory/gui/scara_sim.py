import time
import Tkinter as tk

from core import py_main

parameter_list = [0,1,1,2,3,5,8,13,21,34]*2

print(parameter_list)

OCCURENCE_LIST = []
max_length = 10

def init_scara_sim():
    global OCCURENCE_LIST

    p = py_main.lookup.POSITION_ARRAY_FLAGS

    for i in range(len(p)):
        OCCURENCE_LIST.append(p[i].count(1))

def default_values(gui_object):
    print parameter_list
    print(gui_object)
    print(type(gui_object))
    for i in range(gui_object.param_numbers):
        print i,
        gui_object.label_list[i].set(str(parameter_list[i]))
    
    #gui_object.label_list[5].set(str(677))

def check_string(text):
    global OCCURENCE_LIST
    print("checking string => "+text)
    if(len(text) > max_length):
        return False
    g=[]
    for i in range(len(OCCURENCE_LIST)):
        g.append(text.count(chr(i+65)))
##    print g
##    print OCCURENCE_LIST
    d = [x<=y for x,y in zip(g,OCCURENCE_LIST)]
##    print d
    if False in d:
##        print("BAA-DUM-TSS")
        return False
    return alphabet_checker(text)

def alphabet_checker(text):
    g = []
    g = [x.isalpha() or x.isspace() for x in text]
    if False in g:return False
    if text.count(" ")>1:return False
    return True
    
def called_by_GUI(obj,progress_page,string):
    print("receiving controool")

    py_main.CURRENT_ARRAY = list(string)
    py_main.modify_blocks(obj)
    obj.deiconify()
    progress_page.destroy()
    print("trying to open button")
    print("returning control")

init_scara_sim()