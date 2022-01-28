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
frame = ttk.Frame()
root.geometry('800x600') #1280x1024

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

notebook.add(frame1, text='Brewhouse')
notebook.add(frame2, text='Fermentation Tanks')
notebook.add(frame3, text='Serving Tanks')

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
STANKS = []
fTanks=['FT1','FT2','FT3','FT4']
FTANKS = []

def tankCreator(tanks1,frameNumber,TANKS):
    thread = 1
    xf = 0
    yf = 0
    count = 0
    for i in tanks1:
        if count <= 3:
            pass
        elif count >3:
            count = 0
            xf = 0
            yf += 200
            pass
        i = bh.Fermentation(i,thread,frameNumber)
        i.fermMeter.place(x=xf,y=yf,anchor='nw')
        i.crashButton.place(x=xf+110,y=yf+160,anchor='n')
        i.onButton.place(x=xf+110,y=yf+200,anchor='n')
        i.offButton.place(x=xf+110,y=yf+240,anchor='n')
        xf += 195
        TANKS.append(i)
        count += 1
        thread += 1
#tankCreator(sTanks, frame3, STANKS)
tankCreator(fTanks, frame2, FTANKS)


FTANKS[0].start()
FTANKS[1].start()
FTANKS[2].start()
##############Debug Window###################
output = ScrolledText()
output.place(x = 10, rely = 1.0, height = 50,width = 780, anchor ='sw')
pl = fun.PrintLogger(output)
sys.stdout=pl

################################################
####   MAIN LOOP  ##############################

#i.start()
def update():
    # random number gernating for debuggin.  Set Temp = Thermister
    temp = str(randint(0,212))

    #DS18B20_1 =DS18B20.read_temp(DS18B20.sensors[0]) #read temp sensor

    ### Brew House Updates########
    brewery1.hltMeter.configure(amountused = temp)
    brewery1.bkMeter.configure(amountused = temp)
    brewery1.mashMeter.configure(amountused = temp)

    # FTANKS[0].fermMeter.configure(amountused = FTANKS[0].temp)
    # FTANKS[0].setTemp = 50
    #
    # STANKS[0].fermMeter.configure(amountused = temp)

    root.after(500,update)


########################################################
update()
root.mainloop()
