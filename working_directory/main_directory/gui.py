import sys

WORKING_DIRECTORY = ''
SPLITTING_CHARACTER = ''
if sys.platform.startswith('win') : 
	SPLITTING_CHARACTER = '\{}'.format('')
elif sys.platform.startswith('darwin') : 
	SPLITTING_CHARACTER = '/'


def setup() : 

	def locate_working_directory() : 
		working_directory = ''
		for element in __file__.split(SPLITTING_CHARACTER)[:-2] :
			working_directory += element + '{}'.format(SPLITTING_CHARACTER)
		return working_directory
	
	global WORKING_DIRECTORY
	WORKING_DIRECTORY = locate_working_directory()
	print('working_directory --> ',WORKING_DIRECTORY)
	sys.path.append(WORKING_DIRECTORY)

setup()

import Tkinter as tk
import tkMessageBox
import scara_sim as scara


class Application(tk.Frame):
    
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        self.master.wm_attributes('-topmost', 1)
        self.master.configure(bg='#adff00')
        self.master.title("GUI.....")
        self.master.geometry("200x100-600-400")
        instruction=tk.Label(self,text="Select mode:",bg='#74d600',relief=tk.RAISED,pady=5,borderwidth=3)
        instruction.pack(fill=tk.X)
        tk.Button(self,text="RUN",command=self.new_window,bg='#00d27f').pack(fill=tk.X)
        #tk.Button(self,text="DEBUG",command=self.new_window_1,bg='yellow').pack(fill=tk.X)

    def new_window(self):
        self.master.withdraw()
        RUN()



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
        print(str("hullalala le "))
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
        print("going out of GUI...")
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
        print("\nFlag true in gui")
        

  
    def update_label(self,global_string=''):
        self.variable.set(global_string)
        self.update()
    
    def close_window(self):
        self.destroy()
        self.master.deiconify()
   
            
def main():
    
    Application().mainloop()
    

if __name__ == '__main__':

    main()

# CHANGE -- Functions to be implemented here