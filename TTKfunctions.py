import ttkbootstrap as ttk
from time import sleep as sleep
import sys

###Create Radio Buttons
class RadioCreate:
    """
    Create a Radio Button class
    """
    def __init__(self,name):
        self.name = name

    def radioCreate(dict,frame,xpos,ypos):
        v = ttk.IntVar()
        v.set(1)  # initializing the choice, i.e. Python

        languages = dict

        def ShowChoice():
            print(v.get())
        x1 = xpos
        y1 = ypos
        for language, val in languages:
            x1+= 62

            ttk.Radiobutton(frame,
                          text=language,
                          bootstyle ='danger-toolbutton',
                          width = 6,
                          #padx = 20,
                          variable=v,
                          command=ShowChoice, value=val).place(x=x1,y=y1, anchor='w')




class PrintLogger: # create file like object
    """
    A class to take the output of the terminal window and display it in the GUI
    """
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(ttk.END, text) # write text to textbox
        self.textbox.see(ttk.END)
        

            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass
