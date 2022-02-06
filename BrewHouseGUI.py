import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint
from tkinter.scrolledtext import ScrolledText
import TTKfunctions as fun
import BrewHouseClassDefinitions as bh
from BrewHouseClassDefinitions import tprint
import sys
#import ds18b20testing as DS18B20

temp = 0
setTemp = 0


# root window
root = ttk.Window("Brew", "superhero",resizable=(False, False))
#frame = ttk.Frame()
root.geometry('800x600') #1280x1024

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=0, expand=True)

# create frames
frame1 = ttk.Frame(notebook, width=800, height=580)
frame2 = ttk.Frame(notebook, width=800, height=580)
frame3 = ttk.Frame(notebook, width=800, height=580)
frame4 = ttk.Frame(notebook, width=800, height=580)




frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)




# add frames to notebook

notebook.add(frame1, text='Brewhouse')
notebook.add(frame2, text='Fermentation Tanks')
notebook.add(frame3, text='Serving Tanks')
notebook.add(frame4, text='Debug')



###########################################
####BREW HOUSE#############################
###########################################

brewery1 = bh.Brewhouse('Brewhouse 1',frame1)
#brewery1.meterCreate(frame1)

brewery1.hltMeter.place(x=0,y=0, anchor='nw')
brewery1.bkMeter.place(relx=.5,rely=0, anchor='n')
brewery1.mashMeter.place(relx=1,y=0, anchor='ne')

someDict = [("AUTO", 100), ("MAN", 101), ("OFF", 102)]
fun.RadioCreate.radioCreate(someDict,frame1,250,190)


brewery1.bkSetTempMinusButton.place(x=290,y=210, anchor ='nw')
brewery1.bkSetTempLabel.place(relx=.5,y=210, anchor ='n')
brewery1.bkSetTempPlusButton.place(x=500,y=210, anchor ='ne')

brewery1.bkDutyMinusButton.place(x=290,y=260, anchor ='nw')
brewery1.bkDutyLabel.place(relx=.5,y=260, anchor ='n')
brewery1.bkDutyPlusButton.place(x=500,y=260, anchor ='ne')

brewery1.hltSetTempMinusButton.place(x=20,y=210, anchor ='nw')
brewery1.hltSetTempLabel.place(x=60, y =210, anchor = 'w')
brewery1.hltSetTempPlusButton.place(x=180, y=210, anchor ='ne')



###########################################
####Fermentation/ServingTanks#############################
###########################################
sTanks=['ST1','ST2','ST3','ST4','ST5', 'ST6']

fTanks=['FT1','FT2','FT3','FT4', 'FT5','FT6']


def tankCreator(tanks1,frameNumber):
    thread = 1
    xf = 100
    yf = 0
    count = 0
    for i in tanks1:
        if count <= 3:
            pass
        elif count >3:
            count = 0
            xf = 100
            yf += 210
            pass
        i = bh.Fermentation(i,thread,frameNumber)
        i.labelFrame.place(x=xf-100,y=yf,anchor='nw')

        xf += 200
        count += 1
        thread += 1
        i.daemon = True
        i.start()


tankCreator(fTanks, frame2)



##############Debug Window###################
output = ScrolledText(frame4)
output.pack(fill='both', expand = True)
pl = fun.PrintLogger(output)
sys.stdout=pl

################################################
####   MAIN LOOP  ##############################

#i.start()
def update():
    # random number gernating for debuggin.  Set Temp = Thermister
    temp = str(randint(0,212))


    ### Brew House Updates########
    brewery1.hltMeter.configure(amountused = temp)
    brewery1.bkMeter.configure(amountused = temp)
    brewery1.mashMeter.configure(amountused = temp)



    root.after(500,update)


########################################################
update()
root.mainloop()
