from datetime import datetime


##############################
##############################
##############################
class Fermentation:

    ###Add all the parameters for the Class
    def __init__(self,name):
        self.name = name
        self.tempurature = None
        self.setTemperature = 40
        self.valveState = False

    ###Set the historesist that the tanks can be at with hist
    def pid_loop(self,hist):

        if abs(self.tempurature - self.setTemperature)>hist:
            self.valveState = True
        else:
            self.valveState = False

    ####Call to keep the valve open
    def crash(self):
        self.valveState = True

    ###Call to keep the valve closed
    def alwaysOff(self):
        self.valveState = False

##############################
##############################
##############################
class ServingTank:

    ###Add all the parameters for the Class
    def __init__(self,name):
        self.name = name
        self.tempurature = None
        self.setTemperature = 40
        self.valveState = False

    ###Set the historesist that the tanks can be at with hist
    def pid_loop(self,hist):

        if abs(self.tempurature - self.setTemperature)>hist:
            self.valveState = True
        else:
            self.valveState = False

    ####Call to keep the valve open
    def crash(self):
        self.valveState = True

    ###Call to keep the valve closed
    def alwaysOff(self):
        self.valveState = False


##############################
##############################
##############################
class Brewhouse:

    ####Enter all the parameters for the class
    def __init__(self,name):

        self.name = name

        self.hltTemp =   None
        self.hltSetTemp =   None
        self.hltFloatSw = False
        self.hltElement = False

        self.brewKettleTemp =  None
        self.brewKettleDutyCycle = None
        self.brewKettleFloatSw = False
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


    def mainPumpOn(self, power = 50):
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


def tprint(*args):
    stamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(str(*args) + " : "+stamp)
