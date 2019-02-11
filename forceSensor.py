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
force_list = []

# positive and neg values
def value(val):
    ##Twos compliment to deal with offset and error
    force = -((255 - val) + 1) if val >= 0x80 else val
    return abs(force + 82)

#creates the array of forces
def createForceList(force):
    #appends average to list
    force_list.append(force)
    return force_list

#finds the average of the list given
def averageForce(curr_list):
    total = 0
    #iterates through list to find total value, and thus average
    for x in curr_list:
        total += x
    return(total / currlist.length)

#sets up the GPIO and ADC units
def setup():
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)
    
#finds value from force sensor
def findValues():
    force = value(ADC.read(0))
    return force

#checks to see if the breathing rate is 10% lower than the average
def belowNormalThreshold(curr_avg):
    #calls flag if issue is true
    if curr_avg < userInput.rest_force * 0.9:
        issue = True
    return issue

# will check if the breathing patterns have decreased by over 25% in the past 20 sec
def compareDecrease(curr_avg, prev_avg):
    #calls flag if issue is true
    if curr_avg / prev_avg < 0.75:
        issue = True
    return issue

#infinite loop that will collect and analyze data
def analyzeData():
    while True:
        #will run for 20 seconds
        for i in range(200):
            #creates a list using refined data values
            force_list = createForceList(value(findValues()))
            sleep(0.1)
        #calls for function that finds average of list
        curr_avg =  averageForce(force_list)
        #calls function that will set output depending on inupt
        checkDanger(curr_avg, prev_avg)
        #saves the value obtained so current variables can be reset
        prev_avg = curr_avg
        force_list = []
    
#function will check if any of the dangerous flags were observed, and will set the motor accordingly
def checkDanger(curr_avg, prev_avg):
    # if breathing was abnormally low
    if belowNormalThreshold(curr_avg):
        motor.value = 1.0
    #if there was too large of a decrease
    elif compareDecrease(curr_avg, prev_avg):
        motor.value = 0.8
    #if no issues were found
    else:
        motor.value = 0.0

# force tester function is called in the main function
def force_tester():
    #sets up the hardware
    setup()
    #will call function that runs until keyboard intrupt
    analyzeData()
