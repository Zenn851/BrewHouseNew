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
        print("valveON")
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
                                        frame,
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
        #self.temp = read_temp(self.tempAddress)
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
