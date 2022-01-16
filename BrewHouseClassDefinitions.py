from datetime import datetime
import time
import matplotlib.pyplot as plt
from simple_pid import PID
import ttkbootstrap as ttk


##############################
##############################
##############################
class Fermentation:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,name,frame):

        self.name = name
        self.temperature = None
        self.setTemperature = None
        self.valveState = False

        self.fermMeter = ttk.Meter(
                            master=frame,
                            metersize=180,
                            padding = 20,
                            amountused= self.temperature,
                            textright='°F',
                            amounttotal= 80,
                            metertype='semi',
                            subtext=self.name,
                            bootstyle='primary',
                            interactive=False)
        self.crashButton = ttk.Button(
                            frame,
                            text="CRASH",
                            bootstyle="info-outline-toolbutton",
                            command = self.crash)
        self.onButton = ttk.Button(
                            frame,
                            text="ON",
                            bootstyle="info-outline-toolbutton",
                            command = self.pid_loop)
        self.offButton = ttk.Button(
                            frame,
                            text="OFF",
                            bootstyle="info-outline-toolbutton",
                            command = self.alwaysOff)
    ###Set the historesist that the tanks can be at with hist
    def pid_loop(self):
        if self.temperature or self.setTemperature == None:
            tprint(str(self.name) + "  Temperature or Set Temperature not set properly")
            pass
        elif abs(self.temperature - self.setTemperature)>3:
            self.valveState = True
        else:
            self.valveState = False

    ####Call to keep the valve open
    def crash(self):
        self.valveState = True
        tprint(str(self.name) + "  Crash this mofo to start drinking")

    ###Call to keep the valve closed
    def alwaysOff(self):
        self.valveState = False
        tprint(str(self.name) + "  Tank Turned Off")



##############################
##############################
##############################
class ServingTank:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,name):
        self.name = name
        self.temperature = None
        self.setTemperature = 40
        self.valveState = False

    ###Set the historesist that the tanks can be at with hist
    def pid_loop(self,hist):

        if abs(self.temperature - self.setTemperature)>hist:
            self.valveState = True
        else:
            self.valveState = False

    ####Call to keep the valve open
    def crash(self):
        self.valveState = True
        tprint("Crash this mofo to start drinking")

    ###Call to keep the valve closed
    def alwaysOff(self):
        self.valveState = False

    ####GUI Object Creator
    def meterCreate(self,frame,metersize=180):
            self.fermMeter = ttk.Meter(
                                master=frame,
                                metersize=metersize,
                                padding = 20,
                                amountused= self.temperature,
                                textright='°F',
                                amounttotal= 80,
                                metertype='semi',
                                subtext=self.name,
                                bootstyle='primary',
                                interactive=False)
            self.crashButton = ttk.Button(
                                frame,
                                text="CRASH",
                                bootstyle="info-outline-toolbutton",
                                command = self.crash)


##############################
##############################
##############################
class Brewhouse:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """
    def __init__(self,name):

        self.name = name

        self.hltTemp =   None
        self.hltSetTemp =   0
        self.hltDutyCycle = None
        self.hltFloatSwLow = False
        self.hltFloatSwHi = False
        self.hltElement = False

        self.brewKettleTemp =  None
        self.brewKettleSetTemp = None
        self.brewKettleDutyCycle = None
        self.brewKettleFloatSwLow = False
        self.brewKettleFloatSwHi = False
        self.brewKettleElement = False

        self.mashTemp = None
        self.mashSetTemp = None

        self.exchangeTemp = None


        ###Tuple assumes first variable is on/off, second is DutyCycle
        ###Possible we could just set DC to 0
        self.mainPump = (False, 0)

        ###Tuple assumes first variable is on/off, second is DutyCycle
        ###Possible we could just set DC to 0
        self.spargePump = (False, 0)


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
            tprint("Mashton Circulation on, set temperature: "+str(setTemp))
        else:
            tprint("Water Not at Temp to Circulate")

    def mashOff(self):
        self.mainPump = (False, 0)
        self.mashSetTemp = 155
        tprint("mash ton off")

    def boilDutyCycle(self, duty = 80):
        if self.brewKettleFloatSw == True:
            self.brewKettleElement = True
            self.brewKettleDutyCycle = duty
            tprint("Brew Kettle on, Duty Cyle: "+ str(duty)+"%")
        else:
            self.brewKettleElement = False
            tprint("Water/Wort Needs to Fill")

    #######Set the DutyCyle of the element to 100%
    def boilOn(self):
        if self.brewKettleFloatSw == True:
            self.brewKettleElement = True
            self.brewKettleDutyCycle = 100
            tprint("Brew Kettle on, Duty Cyle: 100%")
        else:
            self.brewKettleElement = False
            tprint("Water Needs to Fill")

    #######Set the DutyCyle of the element to 0%
    def boilOff(self):
        self.brewKettleElement = False
        self.brewKettleDutyCycle = 0
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

    def minusTemp(self):
        self.hltSetTemp -=1
        tprint("Temp minus 1")
        self.hltsetTempLabel['text']="SET TEMP:   " +str(self.hltSetTemp)+ u"\N{DEGREE SIGN}" + "F"

    def plusTemp(self):
        self.hltSetTemp +=1
        tprint("Temp Plus 1")
        self.hltsetTempLabel['text']="SET TEMP:   " +str(self.hltSetTemp)+ u"\N{DEGREE SIGN}" + "F"

    def meterCreate(self,frame):

        self.hltMeter = ttk.Meter(
                    master=frame,
                    metersize= 180,
                    padding = 20,
                    amountused=self.hltTemp, ###########
                    textright='°F',
                    amounttotal=212,
                    metertype='semi',
                    subtext='HLT Temperature', ##############
                    bootstyle='danger',
                    interactive=False
                    )
        self.hltsetTempPlusButton = ttk.Button(frame,
                                    text="+",
                                    bootstyle="danger",
                                    command= self.plusTemp)

        self.hltsetTempMinusButton =ttk.Button(frame,
                                    text="-",
                                    bootstyle="danger",
                                    command= self.minusTemp)

        self.hltsetTempLabel =  ttk.Label(frame,
                                bootstyle ="inverse-danger",
                                text="SET TEMP:   " +str(self.hltSetTemp)+ u"\N{DEGREE SIGN}" + "F")

        self.hltDutyPlusButton =[]

        self.hltDutyMinusButton =[]

        self.hltDutyLabel =     ttk.Label(frame,
                                text="Duty Cycly:   "
                                +str(self.hltDutyCycle)+"%")

        self.bkMeter = ttk.Meter(
                    master=frame,
                    metersize= 180,
                    padding = 20,
                    amountused=self.brewKettleTemp, ###########
                    textright='°F',
                    amounttotal=212,
                    metertype='semi',
                    subtext='Brew Kettle', ##############
                    bootstyle='danger',
                    interactive=False
                    )
        self.bksetTempPlusButton =[]

        self.bksetTempMinusButton =[]

        self.bksetTempLabel =   ttk.Label(frame,
                                text="SET TEMPERATURE:   "
                                +str(self.brewKettleSetTemp)+ u"\N{DEGREE SIGN}" + "F")

        self.bkDutyPlusButton =[]

        self.bkDutyMinusButton =[]

        self.bkDutyLabel =      ttk.Label(frame,
                                text="Duty Cycly:   "
                                +str(self.brewKettleDutyCycle)+"%")

        self.mashMeter = ttk.Meter(
                    master=frame,
                    metersize= 180,
                    padding = 20,
                    amountused=self.mashTemp, ###########
                    textright='°F',
                    amounttotal=212,
                    metertype='semi',
                    subtext='Mash Ton', ##############
                    bootstyle='danger',
                    interactive=False
                    )

        self.setTempPlus =[]

        self.setTempMinus =[]



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
