from Tkinter import *
import tkMessageBox

global_window_background_colour = '#880000'

class variable_displayer_maker:

    def __init__(self, text_file, mode = 'normal', close_command = "close"):
        self.window_initializations()
        self.line_number = 0
        self.close_command = close_command
        self.text_file = text_file
        self.label_list = []

        if(mode == 'instance_mode'):
            self.gui_type = 'instance_mode'
            self.main_funct()
        else:
            self.gui_type = 'normal'
            self.main_funct()

    def main_funct(self):
        k = get_variables(self.text_file)
        print(k)
        self.character_list = k[0]
        self.variable_list = k[1]
        
        self.make_new_frame()
        label_maker("Change variables and click on 'Save' to store changes",relief = "groove").create(self.current_frame,self)
        self.make_new_frame()

        for i in range(len(k[0])):
            label_maker(self.character_list[i]+"\t=",relief = "flat").create(self.current_frame,self)
            
            label1 = label_maker(str(self.variable_list[i]),relief = "flat", pack_expand = True, pack_fill = X)
            self.label_list.append(label1)
            label1.create(self.current_frame,self)
            
            ip_box = input_box_maker(pack_side = RIGHT, width = 40)
            self.entry_box_list.append(ip_box)
            ip_box.create(self.current_frame)
            
            self.make_new_frame()
        button_maker("Save",command = "get_input").create(self.current_frame,self)
        button_maker("close", fg_color = "red", command = self.close_command).create(self.current_frame,self)

        if(self.gui_type == 'normal'):
            self.mainloop_enable()

    def change_vars(self):
        # If no change --> Dont change variables
        for i in range(len(self.input_list)):
            if self.input_list[i] != None:
                try:
                    self.input_list[i] = int(self.input_list[i])
                except:
                    m = message_box("Cannot change variable \""+ self.character_list[i] +"\" to \""+ str(self.input_list[i]) +"\".")
                    continue
                c = check_range(self.character_list[i],self.input_list[i])
                if(c == True):
                    self.variable_list[i] = self.input_list[i]
                    self.label_list[i].update(str(self.variable_list[i]))
                else:
                    m = message_box("Variable \""+ c +"\" could not be changed since it falls outside the desired range")

        save_variables(self.text_file,self.character_list,self.variable_list)
        self.input_list = []

    def window_initializations(self):
        self.root = Tk()

        self.root.configure(background = global_window_background_colour)
        self.root.focus_force()

        ws = self.root.winfo_screenwidth() 
        hs = self.root.winfo_screenheight()
        x = (ws/2) - 100
        y = (hs/2) - 100

        # self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.root.geometry("+%d+%d" % (x,y) )

        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()

        # print (w,h)

        self.entry_box_list = []
        self.input_list = []
    
    def mainloop_enable(self):
        self.root.mainloop()

    def make_new_frame(self):
        new_frame = Frame(self.root, background = global_window_background_colour)
        new_frame.pack(fill = X)
        self.current_frame = new_frame
        self.line_number += 1
    
    def close_window(self):
        self.root.destroy()

    def get_all_inputs(self):
        m = tkMessageBox.askokcancel("Query","Are you sure you want to save these changes ?")
        if(m):
            for obj in self.entry_box_list:
                b = obj.get()
                self.input_list.append(b)
            self.change_vars()

class window_maker:

    def __init__(self,*args):
        self.window_initializations()
        self.line_number = 0
        self.all_objects = args
        # self.root.attributes('-toolwindow', True)

        if(args[0] == 'instance_mode'):
            self.gui_type = 'instance_mode'
            self.all_objects = list(self.all_objects)
            self.all_objects.pop(0)
            self.main_funct()
        else:
            self.gui_type = 'normal'
            self.main_funct()

    def window_initializations(self):
        self.root = Tk()

        self.root.configure(background = global_window_background_colour)
        self.root.focus_force()

        ws = self.root.winfo_screenwidth() 
        hs = self.root.winfo_screenheight()
        x = (ws/2) - 100
        y = (hs/2) - 100

        # self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.root.geometry("+%d+%d" % (x,y) )

        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()

        # print (w,h)

        self.entry_box_list = []
        self.input_list = []

    def mainloop_enable(self):
        self.root.mainloop()

    def main_funct(self):   
        self.make_new_frame()
        
        for obj in self.all_objects:
            if(type(obj) == int):
                # print("That line please")
                self.make_new_frame()
                
                while(self.line_number < obj):
                    empty_label.create(self.current_frame,self)
                    self.make_new_frame()
                    
            elif(obj.name == "button"):
                obj.create(self.current_frame,self)
                # print("creating button...")
            elif(obj.name == "label"):
                obj.create(self.current_frame,self)
                self.last_label = obj
                # print("creating label...")
            elif(obj.name == "input_box"):
                obj.create(self.current_frame)
                # print("creating input_box...")
                self.entry_box_list.append(obj)

        if(self.gui_type == 'normal'):
            self.mainloop_enable()

    def update_last_label(self,text):
        self.last_label.update(text)

    def make_new_frame(self):
        new_frame = Frame(self.root, background = global_window_background_colour)
        new_frame.pack(fill = X)
        # self.frame_array += new_frame
        self.current_frame = new_frame
        self.line_number += 1
    
    def close_window(self):
        self.root.destroy()

    def get_all_inputs(self):
        for obj in self.entry_box_list:
            b = obj.get()
            self.input_list.append(b)

class input_box_maker:
    
    def __init__(self, pack_side = LEFT, width = 20, password_mode = False):
        self.name = "input_box"
        self.pack_side = pack_side
        self.width = width
        self.password_mode = password_mode
    
    def create(self,frame):
        if(self.password_mode):
            self.input_box = Entry(frame, width = self.width, show = "*")
        else:
            self.input_box = Entry(frame, width = self.width)
        self.input_box.pack(side = self.pack_side)

    def get(self):
        text = self.input_box.get()
        if (len(text) == 0):
            return None
        else:
            return text

class label_maker :
    
    def __init__(self, label_name, bg_color = "white", fg_color = "black", relief = "raised", pack_expand = False, pack_fill = NONE):
        self.name = "label"
        self.label_name = label_name
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.relief = relief
        self.pack_expand = pack_expand
        self.pack_fill = pack_fill

    def create(self, frame, win_obj):
        self.parent_window = win_obj
        self.dynamic_variable = StringVar(master = self.parent_window.root)
        self.dynamic_variable.set(self.label_name)

        self.label = Label(frame, textvariable = self.dynamic_variable, bg = self.bg_color, fg = self.fg_color, relief = self.relief, font = "Verdana" )
        self.label.pack(side = LEFT, expand = self.pack_expand, fill = self.pack_fill)

    def update(self,text):
        self.dynamic_variable.set(text)
        
class button_maker:
    
    def __init__(self, text, bg_color = "white", fg_color = 'black', command = "none"):
        self.name = "button"
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        self.command = command
        
    def create(self,frame,win_obj):
        self.parent_window = win_obj
        self.button = Button(frame, text = self.text, bg = self.bg_color, fg = self.fg_color, command = self.do_something)
        self.button.pack(side = LEFT)

    def do_something(self):
        if(self.command == "none"):
            print("I am doing NOTHING")
        elif(self.command == "get_input"):
            self.parent_window.get_all_inputs()
        elif(self.command == "close"):
            self.parent_window.close_window()
        else:
            self.command()

class message_box :

    def __init__(self, text, msg_type = "information"):
        self.name = "message_box"
        self.text = text
        self.create(msg_type)

    def create(self,msg_type):
        if(msg_type == "information"):
            tkMessageBox.showinfo("Information", self.text)
        elif(msg_type == "query"):
            boolean_value = tkMessageBox.askokcancel("Query", self.text)

empty_label = label_maker("  ", bg_color = global_window_background_colour, relief = "flat")
#---------------------------------------------
def get_variables(file_name):
    with open(file_name,'r') as t:
        k = t.read().split("\n")
        for i in range(len(k)): k[i] = int(k[i])
    return [['a','b','c'],k]

def save_variables(file_name,character_list,variable_list):
    with open(file_name,'w') as t:
        for i in range(len(variable_list)-1):
            t.write(str(variable_list[i]) + '\n')
        t.write(str(variable_list[-1]))

def check_range(character,inputted_var):
    if(character == 'a'):
        if(inputted_var<100):
            return True
        else:
            return character
    return True