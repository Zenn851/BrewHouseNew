from datetime import datetime
import matplotlib.pyplot as plt
from simple_pid import PID
import ttkbootstrap as ttk
from time import sleep, perf_counter
import threading
import pandas as pd
#import thingsIO as th
#from random import randint


from ds18b20testing import read_temp
try:
    from sequentdrivers import relayOn, relayOff
except:
    print("Relay libarry not loaded")
    def relayOn(x,y):
        xxx=0
        #print("valveON")
    def relayOff(x,y):
        xxx=1
        #print("valveOFF")

##############################
##############################
##############################
class Fermentation(threading.Thread):
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,name,threadID,frame="frame2",class1= "ferm", tempAddress="28-0721705c2caa",valveBoard=3, valveChannel=1,setTemp = None, mode = "OFF", hys = 2):

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.setTemp = setTemp
        self.valveState = False
        self.mode = mode
        self.tempAddress = tempAddress
        self.temp = read_temp(self.tempAddress)
        self.valveBoard = valveBoard
        self.valveChannel = valveChannel
        self.theme = "secondary"
        self.class1 = class1
        self.hys = hys
        self.running = True
        self.tempFlag = True
        self.frame = frame
        self.setDaemon(True)
        self.start()



        #for the radio buttons to function
        self.v = ttk.IntVar()
        #preset the radiobutton to OFF
        df= pd.read_csv('tankInfo.csv',index_col=0)
        for i in df.index:
            if i == self.name:
                x7= int(df.at[i,'State'])
                self.v.set(x7)
        #self.v.set(300)

        self.labelFrame = ttk.Labelframe(
                                        self.frame,
                                        bootstyle=self.theme,
                                        text = str(self.name),
                                        # height= 300,
                                        # width = 300,
                                        borderwidth=10
                                         )

        self.tempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = str(self.temp) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 70, 'bold'),
                                    bootstyle=self.theme
                                    )

        self.setTempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = "SET TEMP:   " + str(self.setTemp) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 15, 'bold'),
                                    bootstyle=self.theme
                                    )

        def setStartUpConditions(state):
            df= pd.read_csv('tankInfo.csv',index_col=0)
            for i in df.index:
                if i == self.name:
                    df.at[i, 'Mode'] = self.mode
                    df.at[i,'SetTemp'] = self.setTemp
                    df.at[i,'State'] = state
                    df.to_csv('tankInfo.csv')

        def writeSetTemp():
            df= pd.read_csv('tankInfo.csv',index_col=0)
            for i in df.index:
                if i == self.name:
                    df.at[i,'SetTemp'] = self.setTemp
                    df.to_csv('tankInfo.csv')


        def nameCrash():
            self.mode = "ON"
            self.setTemp = 34
            x="Crash"
            setStartUpConditions(100)

            #tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.crashButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="CRASH",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = nameCrash,
                            value = 100,
                            width = 15)

        def ferm():
            self.mode = "ON"
            self.setTemp = 68
            setStartUpConditions(400)
            #tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.fermButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="FERM",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = ferm,
                            value=400,
                            width = 15)

        def serve():
            self.mode = "ON"
            self.setTemp = 38
            setStartUpConditions(500)
            #tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.serveButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="SERVE",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = serve,
                            value=500,
                            width = 30)

        def nameOff():
            self.mode = "OFF"
            self.setTemp = None
            setStartUpConditions(300)
            #tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.offButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="OFF",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = nameOff,
                            value = 300,
                            width =30)
        def increaseSet():
            self.setTemp += 1
            writeSetTemp()
            #tprint(str(self.name) + "Set Temperature Increased to: " + str(self.setTemp))

        self.SetTempPlusButton = ttk.Button(self.labelFrame,
                                    text="+",
                                    bootstyle=self.theme + "outline-toolbutton",
                                    command= increaseSet,
                                    width = 3,
                                    padding =3
                                    )
        def decreaseSet():
            self.setTemp -= 1
            writeSetTemp()
            #tprint(str(self.name) + "Set Temperature Decreased to: " + str(self.setTemp))

        self.SetTempMinusButton =ttk.Button(self.labelFrame,
                                    text="-",
                                    bootstyle=self.theme + "outline-toolbutton",
                                    command= decreaseSet,
                                    width = 3,
                                    padding = 3
                                    )
############################################################
###########################################################
############Debug###########################################
        def increaseSet2():
            self.temp += 1
            #tprint(str(self.name) + "Temperature Increased to: " + str(self.temp))

        self.SetTempPlusButton2 = ttk.Button(self.labelFrame,
                                    text="+",
                                    bootstyle=self.theme + "outline-toolbutton",
                                    command= increaseSet2,
                                    width = 3,
                                    padding =3
                                    )
        def decreaseSet2():
            self.temp -= 1
            #tprint(str(self.name) + "Temperature Decreased to: " + str(self.temp))

        self.SetTempMinusButton2 =ttk.Button(self.labelFrame,
                                    text="-",
                                    bootstyle=self.theme + "outline-toolbutton",
                                    command= decreaseSet2,
                                    width = 3,
                                    padding = 3
                                    )


################################################
        #frame2.pack(fill='both', expand=True)
        self.labelFrame.columnconfigure((0,1,2,3), weight = 1)
        self.labelFrame.rowconfigure(0, weight = 2)
        self.labelFrame.rowconfigure((1,2,3), weight = 1)

        if self.class1 == "ferm":
            self.tempLabel.grid(row=0,column=1,columnspan=2, sticky="n", padx=2,pady=2)

            self.setTempLabel.grid(row=1,column=1, columnspan=2,  sticky="n", padx=2,pady=2)
            self.SetTempPlusButton.grid(row=1,column=3, sticky="nsew", padx=2,pady=2)
            self.SetTempMinusButton.grid(row=1,column=0, sticky="nsew", padx=2,pady=2)

            self.crashButton.grid(row=2,column=0, columnspan=2, sticky="nsew", padx=2,pady=2)
            self.fermButton.grid(row=2,column=2,columnspan=2, sticky="nsew", padx=2,pady=2)

            self.offButton.grid(row=3, columnspan=4, sticky="nsew", padx=2,pady=2)
            ###########DEBUG TEMP BUTTONS######################
            #self.SetTempPlusButton2.grid(row=0,column=3, sticky="ew", padx=2,pady=2)
            #self.SetTempMinusButton2.grid(row=0,column=0, sticky="ew", padx=2,pady=2)
        else:
            self.tempLabel.grid(row=0,column=1,columnspan=2, sticky="n", padx=2,pady=2)

            self.setTempLabel.grid(row=1,column=1, columnspan=2,  sticky="n", padx=2,pady=2)
            self.SetTempPlusButton.grid(row=1,column=3, sticky="nsew", padx=2,pady=2)
            self.SetTempMinusButton.grid(row=1,column=0, sticky="nsew", padx=2,pady=2)

            self.serveButton.grid(row=2, columnspan=4, sticky="nsew", padx=2,pady=2)
            self.offButton.grid(row=3, columnspan=4, sticky="nsew", padx=2,pady=2)

    def updateTemp(self):
        self.temp = read_temp(self.tempAddress)
        #self.temp = randint(50,80)
        #print(self.name + "updated temp")
        return self.temp

    def colorConfigure(self, state):
            self.theme = state
            self.labelFrame.configure(bootstyle =self.theme)
            self.tempLabel.configure(bootstyle =self.theme)
            self.setTempLabel.configure(bootstyle =self.theme)
            self.serveButton.configure(bootstyle =self.theme + "outline-toolbutton")
            self.offButton.configure(bootstyle =self.theme + "outline-toolbutton")
            self.fermButton.configure(bootstyle =self.theme + "outline-toolbutton")
            self.crashButton.configure(bootstyle =self.theme + "outline-toolbutton")
            self.SetTempPlusButton.configure(bootstyle =self.theme + "outline-toolbutton")
            self.SetTempMinusButton.configure(bootstyle =self.theme + "outline-toolbutton")

    #Created a function for the main loop
    def tankTempControl(self):
        self.temp = read_temp(self.tempAddress)
        self.tempLabel['text']= str(self.temp) + u"\N{DEGREE SIGN}"
        self.setTempLabel['text']= text = "SET TEMP:   " + str(self.setTemp) + u"\N{DEGREE SIGN}"

        if self.mode == "ON":
            if self.temp > self.setTemp + .5:
                self.valveState = True
                relayOn(self.valveBoard, self.valveChannel)
                #tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                self.colorConfigure("danger")
                self.tempFlag = True

            elif self.temp > (self.setTemp-self.hys) and self.tempFlag:
                self.valveState = True
                relayOn(self.valveBoard, self.valveChannel)
                #tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                self.colorConfigure("primary")

            elif self.temp <= (self.setTemp -self.hys):
                self.valveState = False
                relayOff(self.valveBoard, self.valveChannel)
                #tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                self.colorConfigure("success")
                self.tempFlag = False

            elif self.temp > (self.setTemp- self.hys) and self.tempFlag == False:
                self.valveState = False
                relayOff(self.valveBoard, self.valveChannel)
                #tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                self.colorConfigure("success")

            else:
                self.valveState = False
                relayOff(self.valveBoard, self.valveChannel)
                #tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                self.colorConfigure("success")


        elif self.mode == "OFF":
            self.valveState = False
            relayOff(self.valveBoard, self.valveChannel)
            #tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
            self.colorConfigure("secondary")


        else:
            tprint("not working, mode must be set incorrectly")


    ######This is the main thread for the class
    def run(self):
        #Initializing
        print ("Run Fermentation Class Thread:  "  + self.name)
        print("Temperature Sencor Address: " + self.tempAddress)
        print("Valve Solenoid Board/Relay: " + str(self.valveBoard) + ", " + str(self.valveChannel))
        print("Previous Set Temperate: "+ str(self.setTemp))
        print("Mode Initialized to : "+ self.mode)
        print("Hysteresis Set Point: "+str(self.hys))

        #Below code delays 10 seconds before reading the temp value
        sleep(10)

        while self.running:
            sleep(1)
            self.tankTempControl()

##############################
##############################

class BoilKettle(threading.Thread):
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,  name="Kettle",
                        threadID=55,
                        frame="frame1",
                        tempAddress="28-0721705c2caa",
                        valveBoard=3,
                        valveChannel=1,
                        setTemp = None,
                        mode = "OFF",
                        hys = 2,
                        auto = 212):

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.setTemp = setTemp
        self.valveState = False
        self.mode = mode
        self.tempAddress = tempAddress
        self.temp = read_temp(self.tempAddress)
        self.valveBoard = valveBoard
        self.valveChannel = valveChannel
        self.theme = "info"
        self.hys = hys
        self.auto = auto


        #######Radio Buttons: Off:100, Man:200, Auto: 300
        self.v = ttk.IntVar()
        self.v.set(100)

        self.labelFrame = ttk.Labelframe(
                                        frame,
                                        bootstyle=self.theme,
                                        text = self.name,
                                        height= 600,
                                        width = 300,
                                        borderwidth=10
                                        )
        self.tempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = str(self.temp) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 50, 'bold'),
                                    bootstyle=self.theme
                                    )

        self.setTempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = "SET TEMP:   " + str(self.setTemp) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 15, 'bold'),
                                    bootstyle=self.theme
                                    )

        def nameOff():
            self.mode = "OFF"
            self.setTemp = None


        self.offButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="OFF",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = nameOff,
                            value = 100,
                            width = 10)
        def nameMan(x=self.auto):
            self.mode = "Man"
            self.setTemp = x


        self.manButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="MAN",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = nameMan,
                            value = 200,
                            width = 10)
        def nameAuto(x=self.auto):
            self.mode = "Auto"
            self.setTemp = x


        self.autoButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="AUTO",
                            bootstyle=self.theme + "outline-toolbutton",
                            variable=self.v,
                            command = nameAuto,
                            value = 300,
                            width = 10)

        def increaseSet():
            self.setTemp += 1
            #writeSetTemp()
            #tprint(str(self.name) + "Set Temperature Increased to: " + str(self.setTemp))

        self.SetTempPlusButton = ttk.Button(self.labelFrame,
                                    text="+",
                                    bootstyle=self.theme + "outline-toolbutton",
                                    command= increaseSet,
                                    width = 3,
                                    padding =3
                                    )
        def decreaseSet():
            self.setTemp -= 1
            #writeSetTemp()
            #tprint(str(self.name) + "Set Temperature Decreased to: " + str(self.setTemp))

        self.SetTempMinusButton =ttk.Button(self.labelFrame,
                                    text="-",
                                    bootstyle=self.theme + "outline-toolbutton",
                                    command= decreaseSet,
                                    width = 3,
                                    padding = 3
                                    )


        self.tempLabel.place(relx=.5, rely=0, anchor ='n')
        self.setTempLabel.place(relx=.5, rely=.15, anchor='n')

        self.offButton.place(relx=.3, rely=.30, height = 50, anchor ='ne')
        self.manButton.place(relx=.50, rely=.30,height = 50, anchor ='n')
        self.autoButton.place(relx= 1, rely=.30,height = 50, anchor ='ne')

        self.SetTempPlusButton.place(relx=1, rely=.15, height = 30, anchor ='ne')
        self.SetTempMinusButton.place(relx=0, rely=.15, height = 30, anchor ='nw')

    def run(self):
        print ("Run Fermentation Class Thread:  "  + self.name)


        while True:
            print("Running"+ self.name +": " + self.mode)

            self.temp = read_temp(self.tempAddress)
            self.tempLabel['text']= str(self.temp) + u"\N{DEGREE SIGN}"
            self.setTempLabel['text']= text = "SET TEMP:   " + str(self.setTemp) + u"\N{DEGREE SIGN}"
            sleep(1)


class MashTon(BoilKettle):
    def __init__(self,name="Mash Ton",
                threadID=55,frame="frame1",
                tempAddress="28-0721705c2caa",
                valveBoard=3,
                valveChannel=1,
                setTemp = None,
                mode = "OFF",
                hys = 2,
                auto= 155):
            super().__init__(name,threadID,frame, tempAddress, valveBoard,valveChannel,setTemp,mode,hys,auto)
            self.theme = "success"
            self.light = ttk.StringVar()
            self.lightButton = ttk.Checkbutton(
                                        self.labelFrame,
                                        text = "LIGHT",
                                        bootstyle=self.theme+"outline-toolbutton",
                                        variable= self.light,
                                        onvalue = "ON",
                                        offvalue = "OFF",
                                        width = 40
                                        )

            self.strike = ttk.StringVar()
            self.strikeButton = ttk.Checkbutton(
                                        self.labelFrame,
                                        text = "STRIKE/SPRAGE",
                                        bootstyle=self.theme+"outline-toolbutton",
                                        variable= self.strike,
                                        onvalue = "ON",
                                        offvalue = "OFF",
                                        width = 40
                                        )

            self.grant = ttk.StringVar()
            self.grantButton = ttk.Checkbutton(
                                        self.labelFrame,
                                        text = "GRANT ENABLE",
                                        bootstyle=self.theme+"outline-toolbutton",
                                        variable= self.grant,
                                        onvalue = "ON",
                                        offvalue = "OFF",
                                        width = 40
                                        )

            self.lightButton.place(relx=.50, rely=.50,height = 50, anchor ='n')
            self.strikeButton.place(relx=.50, rely=.65,height = 50, anchor ='n')
            self.grantButton.place(relx=.50, rely=.80,height = 50, anchor ='n')

class HotLiquorTank(BoilKettle):
    def __init__(self,name="HLT",
                threadID=55,frame="frame1",
                tempAddress="28-0721705c2caa",
                valveBoard=3,
                valveChannel=1,
                setTemp = None,
                mode = "OFF",
                hys = 2,
                auto=170):
            super().__init__(name,threadID,frame, tempAddress, valveBoard,valveChannel,setTemp,mode,hys,auto)
            self.roState = False
            self.cityState = False

            def robutton():
                self.roState = not(self.roState)
                print(self.roState)
                if self.roState:
                    #add function to perfrom
                    self.roButton.configure(bootstyle = "success")
                else:
                    #stop function
                    self.roButton.configure(bootstyle = "success-outline")


            self.roButton = ttk.Button(
                                        self.labelFrame,
                                        bootstyle="success-outline",
                                        text = "R.O. FILL",
                                        width = 40,
                                        command = robutton
                                        )
            def cityButton():
                self.cityState = not(self.cityState)
                print(self.cityState)
                if self.cityState:
                    #add function to perfrom
                    self.cityButton.configure(bootstyle = "success")
                else:
                    #stop function
                    self.cityButton.configure(bootstyle = "success-outline")


            self.cityButton = ttk.Button(
                                        self.labelFrame,
                                        bootstyle="success-outline",
                                        text = "CITY FILL",
                                        width = 40,
                                        command = cityButton
                                        )

            self.flood = ttk.Floodgauge(
                                        self.labelFrame,
                                        bootstyle="success",
                                        text = "Pumping",
                                        length = 250,
                                        maximum = 100,
                                        value = 10
                                        )
            self.scale = ttk.Scale(
                                    self.labelFrame,
                                    bootstyle="info"
                                    )


            self.roButton.place(relx=.50, rely=.50,height = 50, anchor ='n')
            self.cityButton.place(relx=.50, rely=.65,height = 50, anchor ='n')
            self.flood.place(relx=.50, rely=.80,height = 50, anchor ='n')
            #self.scale.place(relx=.50, rely=.85,height = 50, anchor ='n')

class PumpControl(threading.Thread):
    def __init__(self,
                name="Pump",
                frame = "Frame1",
                threadID = None,
                mode = "ON",
                power = 0):

        threading.Thread.__init__(self)
        self.name = name
        self.frame=frame
        self.threadID = threadID
        self.mode = mode
        self.power= power
        self.theme = "primary"


        self.labelFrame = ttk.Labelframe(
                                        self.frame,
                                        bootstyle=self.theme,
                                        text = self.name,
                                        height= 150,
                                        width = 300,
                                        borderwidth=10
                                            )


        self.slider = ttk.Scale(
                                self.labelFrame,
                                bootstyle="info",
                                from_=0,
                                to=100,
                                value =25,
                                length = 250
                                )



        self.setPowerLabel = ttk.Label(
                                    self.labelFrame,
                                    text = "OFF",
                                    borderwidth = 5,
                                    font=("Helvetica", 20, 'bold'),
                                    bootstyle=self.theme
                                    )

        self.var10 = ttk.StringVar()

        self.toggleButton = ttk.Checkbutton(
                                    self.labelFrame,
                                    text = "OFF/ON",
                                    bootstyle=self.theme+"-square-toggle",
                                    variable= self.var10,
                                    onvalue = "ON",
                                    offvalue = "OFF"
                                    )


        self.slider.place(relx=.50, rely=.60,height = 50, anchor ='n')
        self.setPowerLabel.place(relx=.50, rely=.30,height = 50, anchor ='n')
        self.toggleButton.place(relx=.50, rely=0.3,height = 50, anchor ='s')

    def run(self):
        print ("Run Pump Class Thread:  "  + self.name)


        while True:
            print("Running"+ self.name +": " + str(self.mode))
            sleep(1)
            self.mode = self.var10.get()
            if self.mode == "ON":
                self.power=int(self.slider.get())
                print(self.power)
                self.setPowerLabel['text']= str(int(self.slider.get())) + "% Pump Speed"
            elif self.mode == "OFF":
                self.slider.configure(state="diabled")
                self.setPowerLabel['text']= "Pump Off"


class HeatExchange():
    def __init__(
                    self,
                    name,
                    frame,
                    tempAddress1="28-0721705c2caa",
                    tempAddress2="28-0721705c2caa"):

        self.name = name
        self.theme = "light"
        self.tempAddress1 = tempAddress1
        self.temp1 = read_temp(self.tempAddress1)
        self.tempAddress2 = tempAddress2
        self.temp2 = read_temp(self.tempAddress2)
        self.labelFrame = ttk.Labelframe(
                                        frame,
                                        bootstyle = self.theme,
                                        text = self.name,
                                        height = 250,
                                        width = 300,
                                        borderwidth=1,
                                        )


        self.workOutLabel = ttk.Label(
                                    self.labelFrame,
                                    text = "WORK OUT",
                                    borderwidth = 5,
                                    font=("Helvetica", 15, 'bold'),
                                    bootstyle=self.theme
                                    )

        self.workTempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = str(self.temp1) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 30, 'bold'),
                                    bootstyle=self.theme
                                    )
        self.coolingLabel = ttk.Label(
                                    self.labelFrame,
                                    text = "COOLING WATER OUT",
                                    borderwidth = 5,
                                    font=("Helvetica", 15, 'bold'),
                                    bootstyle=self.theme
                                    )

        self.coolingTempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = str(self.temp2) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 30, 'bold'),
                                    bootstyle=self.theme
                                    )

        self.workOutLabel.place(relx=.5, rely=0, anchor ='n')
        self.workTempLabel.place(relx=.5, rely=.10, anchor ='n')
        self.coolingLabel.place(relx=.5, rely=.5, anchor ='n')
        self.coolingTempLabel.place(relx=.5, rely=.6, anchor='n')

def tprint(*args):
    stamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S \n'))
    print(str(*args) + " : "+stamp)

##############
###Example of using the PID control
######################################
if __name__ == '__main__':

    class WaterBoiler:
        """
        Simple simulation of a water boiler which can heat up water
        and where the heat dissipates slowly over time
        """

        def __init__(self):
            self.water_temp = 20

        def update(self, boiler_power, dt):
            if boiler_power > 0:
                # Boiler can only produce heat, not cold
                self.water_temp += 1 * boiler_power * dt

            # Some heat dissipation
            self.water_temp -= 1 * dt
            return self.water_temp

    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(1, 0.01, 0.1, setpoint=water_temp)
    pid.output_limits = (0, 1)

    start_time = time.time()
    last_time = start_time


    # Keep track of values for plotting
    setpoint, y, x = [], [], []

    while time.time() - start_time < 10:
        current_time = time.time()
        dt = current_time - last_time

        power = pid(water_temp)
        print(power)
        time.sleep(.1)
        water_temp = boiler.update(power, dt)

        x += [current_time - start_time]
        y += [water_temp]
        setpoint += [pid.setpoint]

        pid.setpoint = 50
        last_time = current_time

    plt.plot(x, y, label='measured')
    plt.plot(x, setpoint, label='target')
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()
