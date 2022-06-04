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
from push import sendNotification
from datetime import datetime
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
frame2.columnconfigure((0,1,2,3), weight = 1)
frame2.rowconfigure((0,1,2), weight = 1)
frame3.pack(fill='both', expand=True)
frame3.columnconfigure((0,1,2,3), weight = 1)
frame3.rowconfigure((0,1,2), weight = 1)
frame4.pack(fill='both', expand=True)
frame4.columnconfigure((0,1,2,3,4,5,6,7), weight = 1)
frame4.rowconfigure(0, weight = 3)
frame4.rowconfigure((1,2,3,4,5,6,7), weight = 1)

# add frames to notebook
notebook.add(frame2, text='Fermentation Tanks')
notebook.add(frame3, text='Serving Tanks')
notebook.add(frame4, text='Debug')

grid = [(1,0),(1,1),(1,2),(1,3),
        (2,0),(2,1),(2,2),(2,3),
        (3,0),(3,1),(3,2),(3,3),
        (4,0),(4,1),(4,2),(4,3)
        ]

###########################################
####Fermentation/ServingTanks#############################
###########################################

def tankCreator(df):
    global grid
    thread,index1,index2 = 1,0,0
    tanks = []
    for index, row in df.iterrows():
        globals()[index] = bh.Fermentation(index,
                            thread,
                            globals()[row['Frame']],
                            tempAddress = row['TempAddress'],
                            valveBoard = int(row['ValveBoard']),
                            valveChannel = int(row['ValveChannel']),
                            setTemp = row['SetTemp'],
                            class1 = row["Type"],
                            mode = row['Mode'],
                            hys = row['Hys'])
        thread += 1
        if row['Frame'] == "frame2":
            globals()[index].labelFrame.grid(row=grid[index2][0]-1, column=grid[index2][1],sticky='nsew',pady=2,padx=2)
            index2+=1
        elif row['Frame'] == "frame3":
            globals()[index].labelFrame.grid(row=grid[index1][0]-1, column=grid[index1][1],sticky='nsew',pady=2,padx=2)
            index1+=1
        tanks.append(index)
    return tanks
tanks = tankCreator(tankInfo)
print(tanks)


###########################################
##############Debug Window#################
###########################################
output = ScrolledText(frame4)
output.grid(sticky= "nsew", row=0, columnspan=8)
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
clearButton.grid(sticky='nsew', column = 3, columnspan=2,pady=1,padx=1)

###############################################
######Testing thread killing###################
###############################################
# def killThread():
#     FV1.running=False
# killButton = ttk.Button(
#                         frame4,
#                         text = "Kill Thread",
#                         command= killThread,
#                         bootstyle="secondary"
#                         )
# killButton.grid(sticky='n', columnspan=2)
############################################
#############################################


#generate the list of threads open when Initialized
threadsOpen = []
index=0
for thread in threading.enumerate():
    globals()[thread.name+"debug"] = ttk.Button(
                                frame4,
                                text = str(thread.name),
                                bootstyle="success"
                                )



    globals()[thread.name+"debug"].grid(row=grid[index][0]+1, column=grid[index][1]*2, sticky="nsew", pady=1,padx=1, columnspan=2)
    threadsOpen.append(thread.name+"debug")
    index +=1
print("first"+ str(threadsOpen))

################################################
####   MAIN LOOP  ##############################
limiter = 0
alertCounter = 10
alertSent = False

def update():
    global limiter, alertCounter, alertSent


    ###################################################
    ############Thread Fault Detection##################
    ###################################################
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
            threadsOpen.remove(i)
            sendNotification(i + " thread is no longer running " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S \n')))


    #print("loopp"+ str(threadsOpen))
    if limiter <1:
        limiter+=1
        pass
    else:
        watch = len(tanks)
        for i in tanks:
            x = globals()[i].updateTemp()
            sleep(.1)
            if x == 0.0:
                alertCounter += 1
            else:
                watch-=1
                print(watch)
                if watch == 0:
                    alertCounter = 0
        limiter = 0
    ###################################################
    ############Thread Fault Detection##################
    ###################################################
    if alertCounter > 30 and not alertSent:
        sendNotification(" Temperature Not Working Properly " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S \n')))
        alertSent = True

    print("alert " + str(alertCounter))
    root.after(5000,update)
update()
# ########################################################

root.mainloop()
