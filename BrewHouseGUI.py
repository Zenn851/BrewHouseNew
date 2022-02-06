import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint
from tkinter.scrolledtext import ScrolledText
import TTKfunctions as fun
import BrewHouseClassDefinitions as bh
from BrewHouseClassDefinitions import tprint
import pandas as pd
import sys

####read in the tank info
tankInfo = pd.read_csv('tankInfo.csv',index_col=0)
print(tankInfo)



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

def tankCreator(df):
    thread = 1
    col1 = 0
    row1 = 0
    col2 = 0
    row2 = 0
    for index, row in df.iterrows():

        if row['Frame'] == "frame2":
            i = bh.Fermentation(index,
                                thread,
                                frame2,
                                tempAddress = row['TempAddress'],
                                valveAddress = row['ValveAddress'],
                                setTemp = row['SetTemp'],
                                mode = row['Mode'])
            i.daemon = True
            i.start()
            thread += 1
            if col1 < 3:
                i.labelFrame.grid(column = col1, row=row1)
                col1 += 1
            elif col1 == 4:
                col1 = 0
                row1+=1
                i.labelFrame.grid(column = col1, row=row1)
                col1+=1
            else:
                i.labelFrame.grid(column = col1, row=row1)
                col1+=1

        elif row['Frame'] == "frame3":
            i = bh.Fermentation(index,
                                thread,
                                frame3,
                                tempAddress = row['TempAddress'],
                                valveAddress = row['ValveAddress'],
                                setTemp = row['SetTemp'],
                                mode = row['Mode'])
            i.daemon = True
            i.start()
            thread += 1
            if col2 < 3:
                i.labelFrame.grid(column = col2, row=row2)
                col2 += 1
            elif col2 == 4:
                col2 = 0
                row2+=1
                i.labelFrame.grid(column = col2, row=row2)
                col2+=1
            else:
                i.labelFrame.grid(column = col2, row=row2)
                col2+=1

tankCreator(tankInfo)

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
