'''
Hi!
Welcome to BrAsthma! We are delighted you chose to accquire my services!
To allow for BrAsthma to be best catered to your needs, we ask that you input some of your personal data.
The model is currently using average presets, but ideally, we ask specifications that follow your medical needs would allow for optimal function
Your medical professional will be able to complete this one-time preset, and then you'll be good to go
If your breath compression force values, or average heart rate ever change drastically, feel free to update this again for optimal results
'''

rest_bpm = 65
rest_force = 20

def presets():

    while True:
        try:
            rest_bpm = int(input("What is your average resting heartrate (beats per minutes)?" ))
            # print("Your resting heartrate is %s bpm " % (bpm))
            print("your resting heartrate is ", rest_bpm, " bpm")
            correct = input("Is that correct? (Y/N) ")
            if correct.upper() == "Y":
                break
        except ValueError:
            print("You have entered an invalid input, please try again.")


    while True:
        try:
            rest_force = int(input("What is your average breathing force (in Newtons)? " ))
            #print("The force experienced due to your breathing is %s N " % (force))
            print("your average force is ", rest_force, "N")
            correct = input("Is that correct? (Y/N) ")
            if correct.upper() == "Y":
                break
        except ValueError:
            print("You have entered an invalid input, please try again.")
    
    print("Thanks for inputting your data! Notice: This will only last for the duration of the program")
    
