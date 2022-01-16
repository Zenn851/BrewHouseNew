import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint
from tkinter.scrolledtext import ScrolledText
import TTKfunctions as fun
import BrewHouseClassDefinitions as bh
from BrewHouseClassDefinitions import tprint
import sys

temp = 0
setTemp = 0


# root window
root = ttk.Window("Brew", "superhero",resizable=(False, False))
frame = ttk.Frame()
root.geometry('800x600')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=0, expand=True)

# create frames
frame1 = ttk.Frame(notebook, width=800, height=580)
frame2 = ttk.Frame(notebook, width=800, height=580)
frame3 = ttk.Frame(notebook, width=800, height=580)


frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
# add frames to notebook

notebook.add(frame1, text='Brew House')
notebook.add(frame2, text='Fermentation Tanks')
notebook.add(frame3, text='Serving Tanks')

###########################################
####BREW HOUSE#############################
###########################################

brewery1 = bh.Brewhouse('Brew House 1')
brewery1.meterCreate(frame1)

brewery1.hltMeter.place(x=0,y=0, anchor='nw')
brewery1.bkMeter.place(relx=.5,rely=0, anchor='n')
brewery1.mashMeter.place(relx=1,y=0, anchor='ne')

someDict = [("AUTO", 100), ("MAN", 101), ("OFF", 102)]
fun.RadioCreate.radioCreate(someDict,frame1,250,190)
brewery1.hltsetTempPlusButton.place(x=470,y=240, anchor ='w')
brewery1.hltsetTempLabel.place(x=350,y=240, anchor ='w')
brewery1.hltsetTempMinusButton.place(x=310,y=240, anchor ='w')

sethltLabel = ttk.Label(frame1, text="HLT SET TEMPERATURE:   " +str(setTemp)+ u"\N{DEGREE SIGN}" + "F")
sethltLabel.place(x=110, y =180, anchor = 'n')




e = ttk.Entry(frame1)
e.place(x=110, y=200, anchor = 'n')
e.get()
e.insert(0,"")

def myClick():
    setTemp = str(e.get())
    sethltLabel["text"] = "HLT SET TEMPERATURE:  " + str(setTemp) + u"\N{DEGREE SIGN}" + "F"
    tprint("HLT SET TEMPERATURE   " +str(setTemp)+ u"\N{DEGREE SIGN}" + "F")

myButton = ttk.Button(frame1, text="Enter HLT Temperature", bootstyle="info-outline-toolbutton", command=myClick)
myButton.place(x=110, y=235, anchor = 'n')



###########################################
####Fermentation#############################
###########################################

tank88 = bh.Fermentation('Tank 1',frame2)
tank88.fermMeter.place(x=0,y=0,anchor='nw')
tank88.crashButton.place(x=110,y=160,anchor='n')
tank88.onButton.place(x=110,y=200,anchor='n')
tank88.offButton.place(x=110,y=240,anchor='n')

###########################################
####ServingTanks#############################
###########################################
tanks=['tank1','tank2','tank3','tank4']

tank3 = bh.ServingTank('S-Tank 1')
tank3.meterCreate(frame3)
tank3.fermMeter.place(x=0,y=0,anchor='nw')
tank3.crashButton.place(x=110,y=160,anchor='n')



##############Debug Window###################
output = ScrolledText()
output.place(x = 10, rely = 1.0, height = 50,width = 780, anchor ='sw')
pl = fun.PrintLogger(output)
sys.stdout=pl

################################################
####   MAIN LOOP  ##############################


def update():
    # random number gernating for debuggin.  Set Temp = Thermister
    temp = str(randint(0,212))
    ### Brew House Updates########
    brewery1.hltMeter.configure(amountused = temp)
    brewery1.bkMeter.configure(amountused = temp)
    brewery1.mashMeter.configure(amountused = temp)

    tank88.fermMeter.configure(amountused = temp)
    tank3.fermMeter.configure(amountused = temp)

    root.after(1000,update)


########################################################
update()
root.mainloop()
