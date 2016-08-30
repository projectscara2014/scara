from gui.gui_objects import *
from gui.gui_maker import *

global_pass = "m"

from gui import scara_sim as scara

class PASSWORD :
    
    def __init__(self,parent):
        self.master = parent
        label1 = label_maker("Enter Password:")
        ip_box = input_box_maker(password_mode = True)
        ok_pass_button = button_maker("Okay", command = self.compare_password)
        self.main_window = window_maker("instance_mode",label1,3,ip_box,4,ok_pass_button)
        self.main_window.mainloop_enable()
        # self.main_window.mainloop_enable()

    def compare_password(self):
        print("trying to compare_password")
        self.main_window.get_all_inputs()
        if(self.main_window.input_list[-1] == global_pass):
            print("Open SETUP mode")
            self.main_window.close_window()
            s = SETUP(self.master)
        else:
            m = message_box("Incorrect Password")
            self.close_window()

    def close_window(self):
        self.main_window.close_window()
        self.master.deiconify()

class CHILD1 :

    def __init__(self,parent):
        self.master = parent
        self.main_window = variable_displayer_maker("variable.txt",mode = "instance_mode",close_command = self.close_window)

    def close_window(self):
        self.main_window.close_window()
        self.master.deiconify()

class SETUP :

    def __init__(self,parent):
        self.master = parent
        label1 = label_maker("Select one of these options:")
        child1 = button_maker("child1", command = self.child1_window)
        child2 = button_maker("child2", command = self.child2_window)
        back_button = button_maker("Back", command = self.close_window)
        self.main_window = window_maker("instance_mode",label1,3,child1,4,child2,5,back_button)
        # self.main_window.mainloop_enable()

    def child1_window(self):
        print("create child1 window")
        self.main_window.root.withdraw()
        c = CHILD1(self)

    def child2_window(self):
        print("create child2 window")

    def close_window(self):
        self.main_window.close_window()
        self.master.deiconify()
        
    def deiconify(self):
        self.main_window.root.deiconify()

import Tkinter as tk
class RUN(tk.Toplevel):
    
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.configure(bg="#009fff")
        self.wm_attributes('-topmost', 1)
        self.geometry("200x300-600-300")
        self.title("RUN")
        self.string=tk.StringVar()
        self.variable=tk.StringVar()            
        tk.Label(self,text="Enter something:",fg='black',bg='#009fdf').grid(row=0,column=0)
        e1=tk.Entry(self,textvariable=self.string).grid(row=2,column=0,pady=10,padx=10)
        self.button=tk.Button(self)
        self.button.config(text="Okay",command=self.pass_from_GUI,state=tk.NORMAL,bg='#40E0D0')
        self.button.grid(row=10,column=0,pady=5)
        #tk.Label(self,text="").pack(side=tk.TOP)
        tk.Button(self,text="Back to main menu?",command=self.close_window,bg='#b87fed').grid(row=15,column=0,pady=180)
        print str("hullalala le ")
        #self.close_button()
             
    def pass_from_GUI(self):
        text=self.string.get()
        text=text.strip()
        text=text.upper()
        if(scara.check_string(text)):
            self.control_passed(text)
        else:
            self.control_retained()

    def control_passed(self,text):  
        print "going out of GUI..."
        print("passing control")
        self.withdraw()
        t=tk.Toplevel(self)
        t.wm_attributes('-topmost',1)
        t.geometry("200x300-500-300")
        t.configure(bg='#009fdf')
        t.title("PROGRESS..")
        tk.Label(t,text="Progress:",bg='#40E0D0').pack(pady=10)
        tk.Label(t,textvariable=self.variable,background="white",wraplength=109,anchor=tk.W,justify=tk.LEFT,width=15).pack()
        but=tk.Button(t,text="quit",bg='#b87fed',command=lambda:self.quit_win(t))
        but.pack(side=tk.BOTTOM)  
        scara.called_by_GUI(self,t,text)  

    def control_retained(self):
        ## Create an error message box here saying that the text you have
        ## entered cannot be processed. Ask the user to try again
        ## with another text
        self.wm_attributes("-disabled",1)
        tkMessageBox.showwarning(title='Invalid Text',message='Please retry with valid text')
        self.wm_attributes("-disabled",0)
        print("--------control retained--------")
    
    def quit_win(setup_page,progress_page):
        scara.py_main.FLAG = True
        print "\nFlag true in gui"
        
    def update_label(self,global_string=''):
        self.variable.set(global_string)
        self.update()
    
    def close_window(self):
        self.destroy()
        self.master.deiconify()

class MAIN :

    def __init__(self):
        run_button = button_maker("RUN",bg_color = "purple",\
            fg_color ="white", command = self.RUN_window_creator)
        setup_button = button_maker("SETUP", command = self.PASSWORD_window_creator)
        self.main_window = window_maker("instance_mode",setup_button,2,run_button) # object returned after window closed
        self.main_window.mainloop_enable()

    def RUN_window_creator(self):
        self.main_window.root.withdraw()
        r = RUN()
        # r = RUN(self)

    def PASSWORD_window_creator(self):
        self.main_window.root.withdraw()
        p = PASSWORD(self)

    def deiconify(self):
        self.main_window.root.deiconify()
        
def some_fn():
    print("SOME FUNCTION WAS CALLED")
# ----------------------------
# m = MAIN()