from userInput import presets
from gpiozero import PWMOutputDevice
##from max30100 import MAX30100
from mock_max30100 import MockMAX30100 as MAX30100
from time import sleep
import userInput

#will test the bpm_tester
def bpm_tester():
    pulseox = MAX30100()
    #initialize the motor device
    motor = PWMOutputDevice(pin=21,active_high=True)
    motor.value = 0
    count = 0
    # sets the default for the previous heart rate as the avg rest bpm
    prev_avg = userInput.rest_bpm
    cur_avg = userInput.rest_bpm
    # continuously runs until program is called
    while True:
        try:
            pulseox.update() # updates the sensor readings
            bpm = pulseox.get_bpm() # Also Updates the values as well
            avg_bpm = pulseox.get_avg_bpm()
            #Gets the values every 10 seconds, to reduce error
            if count % 400 == 0:
                # makes the current heart rate the average heart rate over the past 10 seconds
                # account for error
                if avg_bpm == None:
                    cur_avg
                    count += 1    
                    sleep(0.01)
                    continue
                cur_avg = avg_bpm
                # checks to see if the current average heart rate is too high
                if cur_avg >= (userInput.rest_bpm * 2) or cur_avg >= 120: 
                    print("your heart rate is too high")
                    motor.value = 1.0
                # checks to see if the average heart rate has changed too much over the past 10 seconds 
                elif (cur_avg / prev_avg) >= 1.4:
                    print("your heart rate raised too fast")
                    motor.value = 0.8
                # if no abnormalities are detected
                else:
                    motor.value = 0
                prev_avg = cur_avg
        except Exception as e:
            print(e)
        count += 1    
        sleep(0.01) # we only get 100 sps so update every 1/100 secs

        
