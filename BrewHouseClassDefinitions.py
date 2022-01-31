from datetime import datetime
import time
import matplotlib.pyplot as plt
from simple_pid import PID
import ttkbootstrap as ttk
from time import sleep, perf_counter
import threading
from random import randint
from ds18b20testing import read_temp
from sequentdrivers import relayOn, relayOff
import os

##############################
##############################
##############################
class Fermentation(threading.Thread):
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,name,threadID,frame,tempAddress="28-0721705c2caa",valveAddress=(3,1)):

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.temp = 12
        self.setTemp = 33.0
        self.valveState = False
        self.mode = None
        self.tempAddress = tempAddress
        self.valveAddress = valveAddress

        #for the radio buttons to function
        self.v = ttk.IntVar()
        #preset the radiobutton to OFF
        self.v.set(300)

        self.labelFrame = ttk.Labelframe(
                                        frame,
                                        bootstyle="success",
                                        text = str(self.name),
                                        height= 200,
                                        width = 200,
                                        borderwidth=10
                                         )

        self.fermMeter = ttk.Label(
                                    self.labelFrame,
                                    text = str(self.temp) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 30, 'bold'),
                                    bootstyle='primary'
                                    )

        self.setTempLabel = ttk.Label(
                                    self.labelFrame,
                                    text = "SET TEMP:   " + str(self.setTemp) + u"\N{DEGREE SIGN}",
                                    borderwidth = 5,
                                    font=("Helvetica", 10, 'bold'),
                                    bootstyle='primary'
                                    )




        def nameCrash():
            self.mode = "CRASH"
            self.setTemp = 34
            tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.crashButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="CRASH",
                            bootstyle="info-outline-toolbutton",
                            variable=self.v,
                            command = nameCrash,
                            value = 100,
                            width = 6.8)
        def namePID():
            self.mode = "PID"
            self.setTemp = 68
            tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.onButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="ON",
                            bootstyle="info-outline-toolbutton",
                            variable=self.v,
                            command = namePID,
                            value=200,
                            width = 6)


        def ferm():
            self.mode = "PID"
            self.setTemp = 68
            tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.serveButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="FERM",
                            bootstyle="info-outline-toolbutton",
                            variable=self.v,
                            command = ferm,
                            value=400,
                            width = 8)

        def serve():
            self.mode = "PID"
            self.setTemp = 42
            tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.fermButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="SERVE",
                            bootstyle="info-outline-toolbutton",
                            variable=self.v,
                            command = serve,
                            value=500,
                            width = 8)

        def nameOff():
            self.mode = "OFF"
            self.setTemp = None
            tprint(str(self.name) + "   Mode:" + str(self.mode))
        self.offButton = ttk.Radiobutton(
                            self.labelFrame,
                            text="OFF",
                            bootstyle="info-outline-toolbutton",
                            variable=self.v,
                            command = nameOff,
                            value = 300,
                            width = 6)
        def increaseSet():
            self.setTemp += 1
            tprint(str(self.name) + "Set Temperature Increased to: " + str(self.setTemp))

        self.SetTempPlusButton = ttk.Button(self.labelFrame,
                                    text="+",
                                    bootstyle="info-outline-toolbutton",
                                    command= increaseSet,
                                    width = 3,
                                    padding =3
                                    )
        def decreaseSet():
            self.setTemp -= 1
            tprint(str(self.name) + "Set Temperature Decreased to: " + str(self.setTemp))

        self.SetTempMinusButton =ttk.Button(self.labelFrame,
                                    text="-",
                                    bootstyle="info-outline-toolbutton",
                                    command= decreaseSet,
                                    width = 3,
                                    padding = 3
                                    )




        self.fermMeter.place(relx=.5, rely=0, anchor ='n')
        self.setTempLabel.place(relx=.5, rely=.45, anchor='n')
        self.offButton.place(relx=.15, rely=.6, anchor ='n')
        self.onButton.place(relx=.5, rely=.6, anchor ='n')
        self.crashButton.place(relx=.85, rely=.6, anchor ='n')

        self.serveButton.place(relx=.25, rely=.8, anchor ='n')
        self.fermButton.place(relx=.75, rely=.8, anchor ='n')

        self.SetTempPlusButton.place(relx=1, rely=.4, height = 30, anchor ='ne')
        self.SetTempMinusButton.place(relx=0, rely=.4, height = 30, anchor ='nw')

    ######This is the main thread for the class
    def run(self):
        print ("Run Fermentation Clss Thread:  "  + self.name)
        while True:


            #self.temp = randint(0,212)  #####Here is where we need to pass in the TempSensor#####
            self.temp = read_temp(self.tempAddress)
            #self.setTemp = randint(0,30)

            self.fermMeter['text']= str(self.temp) + u"\N{DEGREE SIGN}"
            # self.setTempLabel['text']= text = "SET TEMP:   " + str(self.setTemp) + u"\N{DEGREE SIGN}"

            if self.mode == "PID":
                if (self.temp - self.setTemp)>1:
                    self.valveState = True
                    relayOn(self.valveAddress[0], self.valveAddress[1])
                    tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                    sleep(2)
                else:
                    self.valveState = False
                    relayOff(self.valveAddress[0], self.valveAddress[1])
                    #closeValve(valveAddress)
                    sleep(2)

            elif self.mode == "CRASH":
                self.valveState = True
                relayOn(self.valveAddress[0], self.valveAddress[1])
                tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                sleep(2)

            elif self.mode == "OFF":
                self.valveState = False
                relayOff(self.valveAddress[0], self.valveAddress[1])
                tprint(str(self.name) + "   Mode: " + str(self.mode) + "  Value Status = " + str(self.valveState))
                sleep(2)

            else:
                sleep(2)
                pass

##############################
##############################
class Brewhouse:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,name,frame):

        self.name = name

        self.hltTemp =   None
        self.hltSetTemp =   0
        self.hltDutyCycle = 0
        self.hltFloatSwLow = False
        self.hltFloatSwHi = False
        self.hltElement = False

        self.bkTemp =  None
        self.bkSetTemp = 0
        self.bkDutyCycle = 0
        self.bkFloatSwLo = False
        self.bkFloatSwHi = False
        self.bkElement = False

        self.mashTemp = None
        self.mashSetTemp = None

        self.exchangeTemp = None


        ###Tuple assumes first variable is on/off, second is DutyCycle
        ###Possible we could just set DC to 0
        self.mainPump = (False, 0)

        ###Tuple assumes first variable is on/off, second is DutyCycle
        ###Possible we could just set DC to 0
        self.spargePump = (False, 0)

#############
        self.hltMeter = ttk.Meter(
                    master=frame,
                    metersize= 180,
                    padding = 10,
                    amountused=self.hltTemp, ###########
                    textright='°F',
                    amounttotal=212,
                    metertype='semi',
                    subtext='HLT Temperature', ##############
                    bootstyle='danger',
                    interactive=False
                    )
        self.hltSetTempPlusButton = ttk.Button(frame,
                                    text="+",
                                    bootstyle="danger",
                                    command= self.hltPlusTemp,
                                    width = 3,
                                    padding = 10)

        self.hltSetTempMinusButton =ttk.Button(frame,
                                    text="-",
                                    bootstyle="danger",
                                    command= self.hltMinusTemp,
                                    width = 3,
                                    padding = 10)

        self.hltSetTempLabel =  ttk.Label(frame,
                                bootstyle ="inverse-danger",
                                text="SET TEMP:   " +str(self.hltSetTemp)+ u"\N{DEGREE SIGN}" + "F")

        self.hltDutyPlusButton =ttk.Button(frame,
                                    text="+",
                                    bootstyle="danger",
                                    command= self.hltPlusDutyCycle,
                                    width = 3,
                                    padding = 10)

        self.hltDutyMinusButton =ttk.Button(frame,
                                    text="-",
                                    bootstyle="danger",
                                    command= self.hltMinusDutyCylce,
                                    width = 3,
                                    padding = 10)

        self.hltDutyLabel =     ttk.Label(frame,
                                text="Duty Cycly:   "
                                +str(self.hltDutyCycle)+"%")

        self.bkMeter = ttk.Meter(
                    master=frame,
                    metersize= 180,
                    padding = 10,
                    amountused=self.bkTemp, ###########
                    textright='°F',
                    amounttotal=212,
                    metertype='semi',
                    subtext='Brew Kettle', ##############
                    bootstyle='danger',
                    interactive=False
                    )
        self.bkSetTempPlusButton = ttk.Button(frame,
                                    text="+",
                                    bootstyle="danger",
                                    command= self.bkPlusTemp,
                                    width = 3,
                                    padding = 10
                                    )

        self.bkSetTempMinusButton =ttk.Button(frame,
                                    text="-",
                                    bootstyle="danger",
                                    command= self.bkMinusTemp,
                                    width = 3,
                                    padding = 10
                                    )

        self.bkSetTempLabel =   ttk.Label(frame,
                                text="SET TEMP:   "
                                +str(self.bkSetTemp)+ u"\N{DEGREE SIGN}" + "F",
                                width = 14,
                                padding = 10,
                                bootstyle ="inverse-danger"
                                )

        self.bkDutyPlusButton =ttk.Button(frame,
                                    text="+",
                                    bootstyle="danger",
                                    width = 3,
                                    padding = 10,
                                    command= self.bkPlusDutyCycle)

        self.bkDutyMinusButton =ttk.Button(frame,
                                    text="-",
                                    bootstyle="danger",
                                    width = 3,
                                    padding = 10,
                                    command= self.bkMinusDutyCylce)

        self.bkDutyLabel =      ttk.Label(frame,
                                text="Duty Cycly:   "
                                +str(self.bkDutyCycle)+"%")

        self.mashMeter = ttk.Meter(
                    master=frame,
                    metersize= 180,
                    padding = 10,
                    amountused=self.mashTemp, ###########
                    textright='°F',
                    amounttotal=212,
                    metertype='semi',
                    subtext='Mash Tun', ##############
                    bootstyle='danger',
                    interactive=False
                    )

        self.setTempPlus =[]

        self.setTempMinus =[]
#########################

    def mainPumpOn(self, power=50):
        if power < 0 or power >100:
            tprint("Please Enter a Value between 0 and 100")

        else:
            self.mainPump = (True, power)
            tprint("Main Pump Turned on "+str(power)+"% Power")


    def spargePumpOn(self, power = 50):
        if power < 0 or power >100:
            tprint("Please Enter a Value between 0 and 100")

        else:
            self.spargePump = (True, power)
            tprint("Sparge Pump Turned on "+str(power)+"% Power")

    def mashON(self, setTemp = 155):
        if brewKettleFloatSw == True:
            self.mainPump = (True, 50)
            self.mashSetTemp = 155
            tprint("Mash tun Circulation on, set temperature: "+str(setTemp))
        else:
            tprint("Water Not at Temp to Circulate")

    def mashOff(self):
        self.mainPump = (False, 0)
        self.mashSetTemp = 155
        tprint("mash tun off")

    def boilDutyCycle(self, duty = 80):
        if self.bkFloatSwHi == True:
            self.bkeElement = True
            self.bkDutyCycle = duty
            tprint("Brew Kettle on, Duty Cyle: "+ str(duty)+"%")
        else:
            self.bkElement = False
            tprint("Water/Wort Needs to Fill")

    #######Set the DutyCyle of the element to 100%
    def boilOn(self):
        if self.bkFloatSwHi == True:
            self.bkeElement = True
            self.bkDutyCycle = 100
            tprint("Brew Kettle on, Duty Cyle: 100%")
        else:
            self.bkElement = False
            tprint("Water Needs to Fill")

    #######Set the DutyCyle of the element to 0%
    def boilOff(self):
        self.bkElement = False
        self.bkDutyCycle = 0
        tprint("Brew Kettle Off, Duty Cyle: 0%")

    def hltOn(self, setTemp = 180):
        if hltFloatSw == True:
            hltElement = True
            self.hltSetTemp = setTemp
            tprint("HLT Temp Set to " + str(setTemp))
        else:
            print("HLT Tank Needs Water to Start")

    def hltOff(self):
        hltElement = False
        self.hltSetTemp = 0
        tprint("HLT Turned Off")

    def bkMinusTemp(self):
        self.bkSetTemp -=1
        tprint("Bew Kettle Temp minus 1")
        self.bkSetTempLabel['text']="SET TEMP:   " +str(self.bkSetTemp)+ u"\N{DEGREE SIGN}" + "F"

    def bkPlusTemp(self):
        self.bkSetTemp +=1
        tprint("Brew Kettle Temp Plus 1")
        self.bkSetTempLabel['text']="SET TEMP:   " +str(self.bkSetTemp)+ u"\N{DEGREE SIGN}" + "F"

    def hltMinusTemp(self):
        self.hltSetTemp -=1
        tprint("HLT Temp minus 1")
        self.hltSetTempLabel['text']="SET TEMP:   " +str(self.hltSetTemp)+ u"\N{DEGREE SIGN}" + "F"

    def hltPlusTemp(self):
        self.hltSetTemp +=1
        tprint("HLT Temp Plus 1")
        self.hltSetTempLabel['text']="SET TEMP:   " +str(self.hltSetTemp)+ u"\N{DEGREE SIGN}" + "F"

    def bkMinusDutyCylce(self):
        self.bkDutyCycle -=1
        tprint("Bew Kettle DutyCyle minus 1")
        self.bkDutyLabel['text']="DutyCyle:   " +str(self.bkDutyCycle)+  "%"

    def bkPlusDutyCycle(self):
        self.bkDutyCycle +=1
        tprint("Brew Kettle DutyCyle Plus 1")
        self.bkDutyLabel['text']="DutyCyle:   " +str(self.bkDutyCycle)+  "%"

    def hltMinusDutyCylce(self):
        self.hltDutyCycle -=1
        tprint("HLT DutyCyle Plus 1%")
        self.hltDutyLabel['text']="DutyCyle:   " +str(self.hltDutyCycle)+  "%"

    def hltPlusDutyCycle(self):
        self.hltDutyCycle +=1
        tprint("HLT DutyCyle Plus 1%")
        self.hltDutyLabel['text']="DutyCyle:   " +str(self.hltDutyCycle)+  "%"


def tprint(*args):
    stamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
    pid.output_limits = (0, 100)

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
