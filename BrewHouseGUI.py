import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
import TTKfunctions as fun
import BrewHouseClassDefinitions as bh
from BrewHouseClassDefinitions import tprint
import pandas as pd
import sys
from time import sleep as sleep

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
root = ttk.Window("Laneside Brewing", "superhero",resizable=(True,True))
root.geometry(str(windowWidth)+"x"+str(windowHeight)) #1280x1024, 800x600
try:
    root.iconbitmap(r'assets\Untitled.ico')
except:
    pass
# create a notebook
notebook = ttk.Notebook(root)
notebook.pack()

# create frames
#frame1 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)
frame2 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)
frame3 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)
frame4 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)

#pack
#frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)

# add frames to notebook

notebook.add(frame2, text='Fermentation Tanks')
notebook.add(frame3, text='Serving Tanks')
notebook.add(frame4, text='Debug')
#notebook.add(frame1, text='Brewhouse')

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
            index = bh.Fermentation(index,
                                thread,
                                frame2,
                                tempAddress = row['TempAddress'],
                                valveBoard = int(row['ValveBoard']),
                                valveChannel = int(row['ValveChannel']),
                                setTemp = row['SetTemp'],
                                class1 = row["Type"],
                                mode = row['Mode'],
                                hys = row['Hys'])
            index.setDaemon(True)
            thread += 1
            if col1 < 3:
                index.labelFrame.grid(column = col1, row=row1)
                col1 += 1
            elif col1 == 4:
                col1 = 0
                row1+=1
                index.labelFrame.grid(column = col1, row=row1)
                col1+=1
            else:
                index.labelFrame.grid(column = col1, row=row1)
                col1+=1
            index.start()
        elif row['Frame'] == "frame3":
            index = bh.Fermentation(index,
                                thread,
                                frame3,
                                tempAddress = row['TempAddress'],
                                valveBoard = int(row['ValveBoard']),
                                valveChannel = int(row['ValveChannel']),
                                setTemp = row['SetTemp'],
                                class1 = row["Type"],
                                mode = row['Mode'],
                                hys = row['Hys'])
            index.setDaemon(True)
            index.start()
            thread += 1
            if col2 < 3:
                index.labelFrame.grid(column = col2, row=row2)
                col2 += 1
            elif col2 == 4:
                col2 = 0
                row2+=1
                index.labelFrame.grid(column = col2, row=row2)
                col2+=1
            else:
                index.labelFrame.grid(column = col2, row=row2)
                col2+=1
        tanks.append(index)
    return tanks
tanks = tankCreator(tankInfo)
###########################################
##############Debug Window#################
###########################################
output = ScrolledText(frame4)
output.pack(fill='both', expand = True)
pl = fun.PrintLogger(output)
sys.stdout=pl

################################################
####   MAIN LOOP  ##############################
# def update():
#    root.after(2000,update)
# update()
# ########################################################

root.mainloop()
