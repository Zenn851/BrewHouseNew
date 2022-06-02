import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
import TTKfunctions as fun
import BrewHouseClassDefinitions as bh
from BrewHouseClassDefinitions import tprint
import pandas as pd
import sys
import threading
from time import sleep as sleep
#import thingsIO as th

####read in the tank info
try:
    tankInfo = pd.read_csv('tankInfo.csv',index_col=0)
except:
    print("failed to open tank info.  Attentemting again")
    sleep(5)
    tankInfo = pd.read_csv('tankInfo.csv',index_col=0)

print(tankInfo)

windowHeight =1024
windowWidth = 1280
# root window
root = ttk.Window("Laneside Brewing: Tank Controller", "superhero",resizable=(True,True))
root.geometry(str(windowWidth)+"x"+str(windowHeight)) #1280x1024, 800x600
try:
    root.iconbitmap(r'assets\Untitled.ico')
except:
    pass
# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# create frames
frame2 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)
frame3 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)
frame4 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)

#pack
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)
frame4.columnconfigure(0, weight = 1)

# add frames to notebook
notebook.add(frame2, text='Fermentation Tanks')
notebook.add(frame3, text='Serving Tanks')
notebook.add(frame4, text='Debug')


###########################################
####Fermentation/ServingTanks#############################
###########################################

def tankCreator(df):
    thread = 1
    col1 = 0
    row1 = 0
    col2 = 0
    row2 = 0
    tanks = []
    for index, row in df.iterrows():
        if row['Frame'] == "frame2":
            globals()[index] = bh.Fermentation(index,
                                thread,
                                frame2,
                                tempAddress = row['TempAddress'],
                                valveBoard = int(row['ValveBoard']),
                                valveChannel = int(row['ValveChannel']),
                                setTemp = row['SetTemp'],
                                class1 = row["Type"],
                                mode = row['Mode'],
                                hys = row['Hys'])
            #index.setDaemon(True)
            thread += 1
            if col1 < 3:
                globals()[index].labelFrame.grid(column = col1, row=row1)
                col1 += 1
            elif col1 == 4:
                col1 = 0
                row1+=1
                globals()[index].labelFrame.grid(column = col1, row=row1)
                col1+=1
            else:
                globals()[index].labelFrame.grid(column = col1, row=row1)
                col1+=1
            #index.start()
        elif row['Frame'] == "frame3":
            globals()[index] = bh.Fermentation(index,
                                thread,
                                frame3,
                                tempAddress = row['TempAddress'],
                                valveBoard = int(row['ValveBoard']),
                                valveChannel = int(row['ValveChannel']),
                                setTemp = row['SetTemp'],
                                class1 = row["Type"],
                                mode = row['Mode'],
                                hys = row['Hys'])
            #index.setDaemon(True)
            #index.start()
            thread += 1
            if col2 < 3:
                globals()[index].labelFrame.grid(column = col2, row=row2)
                col2 += 1
            elif col2 == 4:
                col2 = 0
                row2+=1
                globals()[index].labelFrame.grid(column = col2, row=row2)
                col2+=1
            else:
                globals()[index].labelFrame.grid(column = col2, row=row2)
                col2+=1
        tanks.append(index)
    return tanks
tanks = tankCreator(tankInfo)
print(tanks)


###########################################
##############Debug Window#################
###########################################
output = ScrolledText(frame4)
output.grid(column=0, row=0, sticky="EW")
pl = fun.PrintLogger(output)
sys.stdout=pl
def clearBox():
    pl.clearText()
clearButton = ttk.Button(
                        frame4,
                        text = "Clear",
                        command= clearBox,
                        bootstyle="secondary"
                        )
clearButton.grid(sticky='n')
#generate the list of threads open when Initialized
threadsOpen = []
for thread in threading.enumerate():
    globals()[thread.name+"debug"] = ttk.Button(
                                frame4,
                                text = str(thread.name),
                                bootstyle="success"
                                )
    globals()[thread.name+"debug"].grid(sticky='w')
    threadsOpen.append(thread.name+"debug")


################################################
####   MAIN LOOP  ##############################
def update():

    #create a list of the active threads openb
    currentThreads = []
    for thread in threading.enumerate():
        currentThreads.append(thread.name+"debug")


    #check the current theads against the threads that were open
    for i in threadsOpen:
        if i in currentThreads:
            globals()[i].configure(bootstyle="success")
        else:
            globals()[i].configure(bootstyle="danger")
            print (i + " is not running")


    for i in tanks:
        globals()[i].updateTemp()
        sleep(.1)

    root.after(10000,update)
update()
# ########################################################

root.mainloop()
