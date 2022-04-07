import lib8mosind as OUTPUTS
import megaind as IO
import librtd as RTD
import lib8relind as RELAYS
import time
import RPi.GPIO as GPIO

wortGrantFloat = 5 #define GPIO inputs for float switches
HLTfloatLow = 6
HLTfloatHigh = 7
CLTfloatLow = 8
CLTfloatHigh = 9
kettleFloat =10
#HLTfloatIsFilled = False



DS18b20_1 = "28-0721705c2caa"

GPIO.setmode(GPIO.BCM) # Use Broadcom numbers not Pi pin numbers
#Set all float switches as pulldown inputs
GPIO.setup(wortGrantFloat, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HLTfloatLow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HLTfloatHigh, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLTfloatLow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLTfloatHigh, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(kettleFloat, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Led assignments for tank controls- these do not control tanks- Sequent relay board does



#Stack address of Sequent Microsystems boards 0 is closest to Pi- assigned by jumpers on boards- maximum of 8 boards
RTD_board = 0 #RTD board
MOS_board = 1 #MOSFET 8 channel board
MEGA_board = 2 # Mega board with many inputs/outputs
FV_board = 3 #8 relay board for fermentation tanks
ST_board = 4 #8 relay board for serving/brite tanks




## Assign numbers to RTD temperature sensors corresponding to channel numbers on Sequent Micorsystems RTD 8 channel board
HLT_RTD = 1
MLT_RTD = 2
KET_RTD = 3
HEX_RTD = 4
H2O_RTD = 5 #input water temperature sensor
#RESERVED = 6
#RESERVED = 7
#RESERVED = 8



#Sequent Microsystems Mega Industrial Automation board assignemnts
#
#
#4-20mA inputs
#0-10v inputs
#opto inputs
#4-20mA outputs

#0-10v outputs
spargePump = 1
mashPump = 2
kettlePump = 3
#reserved = 4
#

#open drain outputs
HLTcontactor = 1
kettleContactor = 2


#Sequent Microsystems 8-channel MOSFET board
roFilterPower = 1
auxOutlet = 2
#reserved = 3
#reserved = 4
roHLTfillSolenoid = 5
cityROfillSolenoid = 6
roCLTfillSolenoid = 7
#reserved = 8

def getHLTtemp():
    return RTD.get(RTD_board, HLT_RTD)

def getKettletemp():
    return RTD.get(RTD_board, KET_RTD)

def getMashtemp():
    return RTD.get(RTD_board, MLT_RTD)

def getHEXOutputTemp():
    return RTD.get(RTD_board, HEX_RTD)

def getHEXH2Otemp():
    return RTD.get(RTD_board, H2O_RTD)


#Turns HLT 24vdc contactor on. 24vdc runs through float switch to protect elements. If water level is too low, contactor will not enable.
def HLTSeton():
    IO.setOdPWM(MEGA_board, HLTcontactor, 100)
    print("HLT elements turned on.")
    HLTon = True
    #Need to add 3 variables to turn 3 SSRs on individually because only 2 will be on when Kettle is on

def HLTSetoff():
    IO.setOdPWM(MEGA_board, HLTcontactor, 0)
    print("HLT elements turned off.")
    HLTon = False


#Turns kettle 24vdc contactor on. 24vdc runs through float switch to protect elements. If water level is too low, contactor will not enable.
def kettleSetOn():
    IO.setOdPWM(MEGA_board, kettleContactor, 100)
    print("Kettle elements turned on.")
    kettleOn = True

def kettleSetOff():
    IO.setOdPWM(MEGA_board, kettleContactor, 0)
    print("Kettle elements turned off.")
    kettleOn = False

def fillHLT_withRO():

    #add if statement to check HLT full or not1

    OUTPUTS.set(MOS_board, roFilterPower, 1)
    OUTPUTS.set(MOS_board, roHLTfillSolenoid, 1)
    print("Fill HLT with RO water")

def fillHLT_withCity():
    OUTPUTS.set(MOS_board, cityROfillSolenoid, 1)
    print("Fill HLT with city water")

#turns off RO filter, HLT RO solenoid, HLT city solenoid
def stopHLTFill():
    OUTPUTS.set(MOS_board, roFilterPower, 0)
    OUTPUTS.set(MOS_board, roHLTfillSolenoid, 0)
    OUTPUTS.set(MOS_board, cityROfillSolenoid, 0)
    print("Stop HLT fill.")

def setHLTPump(HLTPumpSpeed): #duty cycle passed from python GUI. May need to divide by 10 to get 0-10v value
    IO.set0_10Out(MEGA_board, HLTPump, HLTPumpSpeed)

def setMashPump(mashPumpSpeed): #duty cycle passed from python GUI. May need to divide by 10 to get 0-10v value
    IO.set0_10Out(MEGA_board, mashPump, mashPumpSpeed)

def setKettlePump(kettlePumpSpeed): #duty cycle passed from python GUI. May need to divide by 10 to get 0-10v value
    IO.set0_10Out(MEGA_board, kettlePump, kettlePumpSpeed)

def getHLTfloatLow():
    HLTfloatIsFilled = GPIO.input(HLTfloatLow)
    return HLTfloatIsFilled

def getHLTfloatHigh():
    return GPIO.input(HLTfloatHigh)

def FVTankOnTEST(j):
    RELAYS.set(FV_board, j, 1) #for Sequent 8 relay board
    print("tank on")
    #GPIO.output(FV1, GPIO.HIGH)

def FVTankOffTEST(j):
    RELAYS.set(FV_board, j, 0) #for Sequent 8 relay board
    print("tank off")
    #GPIO.output(FV1, GPIO.LOW)

def testRelayBoard():
    i = 1
    while i <= 8:
        FVTankOnTEST(i)

        time.sleep(.5)

        FVTankOffTEST(i)

        time.sleep(.5)
        i += 1



def relayOn(boardNumber,channelNumber):
    try:
        RELAYS.set(boardNumber,channelNumber,1)
    except:
        print("Relay Not Working")

def relayOff(boardNumber,channelNumber):
    try:
        RELAYS.set(boardNumber,channelNumber,0)
    except:
        print("Relay Not Working")




if __name__ == "__main__":

    #print(IO.getFwVer(2))
    #OUTPUTS.set(1, 1, 1)

    #print(IO.getFwVer(3))

    #OUTPUTS.set(3, 4, 1)
    #print(IO.get0_10In(2, 1)) #gets voltage from 0-10V input on IO board ID#2

    #print(RTD.get(RTD_board, HLT_RTD)) #get temperature from RTD board ID#0 channel 1


    #print(getHLTtemp()) #prints HLTtemp returnd by getHLTtemp()
    #HLTSeton() #turn HLT contactor on- still have to turn on solid state relays seperately
    #kettleSetOn()
    #fillHLT_withRO()
    #fillHLT_withCity()

    #stopHLTFill()
    #HLTSetoff()
    print("Running")

    #while True:
