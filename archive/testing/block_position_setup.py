import Tkinter as tk

DYNA_POS_1 = 0x00 #change to dynamixel.DYNA_POS_1
DYNA_POS_2 = 0x00 #change to dynamixel.DYNA_POS_2

def on_key_press(event):

    global DYNA_POS_1,DYNA_POS_2

    def char_to_int(character) :
        for i in range(256) :
            if chr(i) == character :
                return i
        return 256

    def move(dynamixel,keypress) :

        global DYNA_POS_1,DYNA_POS_2
        
        if dynamixel == 1 :
            if(keypress == 97) :
                DYNA_POS_1 -= 1
            elif keypress == 100 :
                DYNA_POS_1 += 1
            else :
                print('press either a or d')

        elif dynamixel == 2 :
            if(keypress == 97) :
                DYNA_POS_2 -= 1
            elif keypress == 100 :
                DYNA_POS_2 += 1
            else :
                print('press either a or d')

        else :
            print('invalid dynamixel ID')
        print(dynamixel is DYNA_POS_1)
        
        text.insert('end','current dynamixel positions : \n dynamixel1 --> {0}\ndynamixel2 --> {1}\n\n'.format(DYNA_POS_1,DYNA_POS_2))
        #dynamixel1.write(DYNA_POS_1) --> EQUIVALENT
        #dynamixel2.write(DYNA_POS_2) --> EQUIVALENT
        
    keypress = char_to_int(event.char)
    move(1,keypress)
    
root = tk.Tk()
root.geometry('600x400')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', on_key_press)
root.mainloop()
