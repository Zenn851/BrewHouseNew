import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint
from tkinter.scrolledtext import ScrolledText
import TTKfunctions as fun
import BrewHouseClassDefinitions as bh
import sys




temp = 0
setTemp = 0

print("h")

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


output = ScrolledText()
output.place(x = 10, rely = 1.0, height = 50,width = 780, anchor ='sw')
pl = fun.PrintLogger(output)
sys.stdout=pl


ping_meter = ttk.Meter(
    master=frame1,
    metersize= 180,
    padding = 20,
    amountused=temp,
    textright='°F',
    amounttotal=212,
    metertype='semi',
    subtext='HLT Temperature',
    bootstyle='danger',
    interactive=False
)
ping_meter.place(x=0,y=0, anchor='nw')


ping_meter1 = ttk.Meter(
    master=frame1,
    metersize= 180,
    padding=20,
    amountused=50,
    textright='°F',
    amounttotal=180,
    metertype='semi',
    subtext='Brew Kettle',
    bootstyle='danger',
    interactive=True
)
ping_meter1.place(relx=.5,rely=0, anchor='n')


someDict = [("AUTO", 100), ("MANUAL", 101), ("OFF", 102)]
fun.RadioCreate.radioCreate(someDict,frame1,400,180)

ping_meter2 = ttk.Meter(
    master=frame1,
    metersize= 180,
    padding=20,
    amountused=50,
    textright='°F',
    amounttotal=180,
    metertype='semi',
    subtext='MASH',
    bootstyle='danger',
    interactive=False
)
ping_meter2.place(relx=1,y=0, anchor='ne')

sethltLabel = ttk.Label(frame1, text="HLT SET TEMPERATURE:   " +str(setTemp)+ u"\N{DEGREE SIGN}" + "F")
sethltLabel.place(x=110, y =180, anchor = 'n')




e = ttk.Entry(frame1)
e.place(x=110, y=200, anchor = 'n')
e.get()
e.insert(0,"")

def myClick():
    setTemp = str(e.get())
    sethltLabel["text"] = "HLT SET TEMPERATURE:  " + str(setTemp) + u"\N{DEGREE SIGN}" + "F"
    print("GPIO 1 Toggle")

myButton = ttk.Button(frame1, text="Enter HLT Temperature", bootstyle="info-outline-toolbutton", command=myClick)
myButton.place(x=110, y=235, anchor = 'n')


################################################################
#################################################################
def update():
    # random number gernating for debuggin.  Set Temp = Thermister
    temp = str(randint(0,212))
    #hltLabel["text"] = "HLT TEMPERATURE:  "+str(temp)+ u"\N{DEGREE SIGN}" + "F"
    ping_meter.configure(amountused = temp)
    tank88.temperature = temp
    root.after(1000,update)
    #print(tank88.temperature)


###########################################
####Fermentation#############################
###########################################
tank88 = bh.Fermentation("Tank1")
tank88.meterCreate(frame2,x=200,y=200,a='w')




###########################################
####ServingTanks#############################
###########################################
tanks=['tank1','tank2','tank3','tank4']

def tankCreator(tanks):
    xpos = 0
    ypos = 0
    for i in tanks:
        tank = ttk.Meter(
            master=frame3,
            metersize= 180,
            padding = 20,
            amountused=40,
            textright='°F',
            amounttotal=212,
            metertype='semi',
            subtext=str(i),
            bootstyle='primary',
            interactive=False
        )
        tank.place(x=xpos,y=ypos, anchor='nw')
        xpos += 200
tankCreator(tanks)




########################################################
update()

root.mainloop()
