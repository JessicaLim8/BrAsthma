#imports required files
import PCF8591_3 as ADC
import RPi.GPIO as GPIO
from time import sleep
import math
from gpiozero import PWMOutputDevice
import userInput

#define inital values
DO = 17
GPIO.setmode(GPIO.BCM)
motor = PWMOutputDevice(pin=15,active_high=True)
force = 0
curr_avg = userInput.rest_force
prev_avg = userInput.rest_force
issue = False

# positive and neg values
def value(val, offset):
    ##Twos compliment to deal with offset and error
    force = -((255 - val) + 1) if val >= 0x80 else val
    return (abs(force) - offset)

#creates the array of forces
def createForceList(force, force_list):
    #appends average to list
    force_list.append(force)
    return force_list

#finds the average of the list given
def averageForce(force_list):
    total = 0
    #iterates through list to find total value, and thus average
    for x in force_list:
        total += x
    return(total / len(force_list))

#sets up the GPIO and ADC units
def setup():
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)
    
#finds value from force sensor
def findValues(offset):
    force = abs(value(ADC.read(0), offset))
    return force

#checks to see if the breathing rate is 10% lower than the average
def belowNormalThreshold(curr_avg):
    #calls flag if issue is true
    issue = False
    if curr_avg < 5:
        issue = True
    return issue

# will check if the breathing patterns have decreased by over 25% in the past 20 sec
def compareDecrease(curr_avg, prev_avg):
    #calls flag if issue is true
    issue = False
    if abs(curr_avg / prev_avg) < 0.85:
        issue = True
    return issue

#infinite loop that will collect and analyze data
def analyzeData(curr_avg, prev_avg, offset):
    while True:
        force_list = []
        #will run for 4 seconds (although in real life, 20 sec)
        for i in range(40):
            #creates a list using refined data values
            force_list = createForceList(findValues(offset), force_list)
            sleep(0.1)
        #calls for function that finds average of list
        curr_avg =  averageForce(force_list)
        #calls function that will set output depending on inupt
        checkDanger(curr_avg, prev_avg)
        #saves the value obtained so current variables can be reset
        prev_avg = curr_avg
    
#function will check if any of the dangerous flags were observed, and will set the motor accordingly
def checkDanger(curr_avg, prev_avg):
    #if there was too large of a decrease
    if compareDecrease(curr_avg, prev_avg) == True:
        motor.value = 0.5
        print("1. The force decreased too fast")
    # if breathing was abnormally low
    elif belowNormalThreshold(curr_avg) == True:
        motor.value = 1.0
        print("1. There is not enough force")
    
    #if no issues were found
    else:
        motor.value = 0.0
        print("1. Your breathing force is fine")

#determine the offset
def checkOffset():
    total = 0
    #uses the first 2 seconds for callibration of force = 0
    for i in range(20):
        total += findValues(0)
    return total / 20

# force tester function is called in the main function
def force_tester():
    offset = 0
    #sets up the hardware
    setup()
    # will initialize the sensor at zero
    offset = checkOffset() - 1
    #will call function that runs until keyboard intrupt
    analyzeData(curr_avg, prev_avg, offset)
