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

windowHeight =1080
windowWidth = 1920
# root window
root = ttk.Window("Laneside Brewing: Brew House Controller", "vapor",resizable=(True,True))
root.geometry(str(windowWidth)+"x"+str(windowHeight)) #1280x1024, 800x600
try:
    root.iconbitmap(r'assets\Untitled.ico')
except:
    pass
# create a notebook
notebook = ttk.Notebook(root)
notebook.pack()

# create frames
frame1 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)
frame4 = ttk.Frame(notebook, width=windowWidth, height=windowHeight)

#pack
frame1.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)

# add frames to notebook
notebook.add(frame1, text='Brewhouse')
notebook.add(frame4, text='Debug')

for index, row in tankInfo.iterrows():
    if row['TempAddress'] == "28-09217063caaa":
        index = bh.Fermentation(index,
                            1,
                            frame1,
                            tempAddress = row['TempAddress'],
                            valveBoard = int(row['ValveBoard']),
                            valveChannel = int(row['ValveChannel']),
                            setTemp = row['SetTemp'],
                            class1 = row["Type"],
                            mode = row['Mode'],
                            hys = row['Hys'])
        index.setDaemon(True)
        index.labelFrame.grid(column = 0, row=0, sticky ="nw")
        index.start()

house = bh.BoilKettle(frame=frame1)
house.setDaemon(True)
house.labelFrame.grid(column = 1, row=0)
house.start()


mash = bh.MashTon(frame=frame1)
mash.setDaemon(True)
mash.labelFrame.grid(column = 2, row=0)
mash.start()

hlt = bh.HotLiquorTank(frame=frame1)
hlt.setDaemon(True)
hlt.labelFrame.grid(column = 3, row=0)
hlt.start()

clt = bh.PumpControl(name ="CLT Pump", frame=frame1)
clt.labelFrame.grid(column = 0, row = 1)

clt = bh.PumpControl(name ="Kettle Pump", frame=frame1)
clt.labelFrame.grid(column = 1, row = 1)

clt = bh.PumpControl(name ="Mash Pump", frame=frame1)
clt.labelFrame.grid(column = 2, row = 1)

clt = bh.PumpControl(name ="HLT Pump", frame=frame1)
clt.labelFrame.grid(column = 3, row = 1)

hex = bh.HeatExchange(name = "HEX", frame = frame1)
hex.labelFrame.grid(column = 0, row = 0, stick="sw")

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
