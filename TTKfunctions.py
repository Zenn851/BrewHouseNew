import ttkbootstrap as ttk
import sys

###Create Radio Buttons
def radioCreate(dict,frame,xpos,ypos):
    v = ttk.IntVar()
    v.set(1)  # initializing the choice, i.e. Python

    languages = dict

    def ShowChoice():
        print(v.get())
    x1 = xpos
    y1 = ypos
    for language, val in languages:
        y1+= 30

        ttk.Radiobutton(frame,
                      text=language,
                      bootstyle ='danger-toolbutton',
                      width = 20,
                      #padx = 20,
                      variable=v,
                      command=[],
                      value=val).place(x=x1,y=y1, anchor='n')



class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(ttk.END, text) # write text to textbox
        self.textbox.see(ttk.END)
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass
