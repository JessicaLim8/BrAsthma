from userInput import presets
from Pulse import bpm_tester
from forceSensor import force_tester
from _thread import start_new_thread

#will run the start up menu
def startup():
    print("Welcome to BrAsthma!")
    while True:
        # will check to see what program the user wants to run
        try:
            program = int(input("To run the program, press 1; \n To change presets, press 2; \n To quit, press 3"))
            #runs main
            if program == 1:
                print("Remember, you can press ctrl C anytime to quit")
                main()
                break
            #runs presets
            elif program == 2:
                presets()
            #stops program
            elif program == 3:
                break
            #catches invalid numbers
            else:
                print("Please try again")
        #catches anything that isnt a number
        except ValueError:
            print("Please try again")

#will run the two programs asynchronously, allowing for all readings and calculations to occur at once
def main():
    try:
        start_new_thread(bpm_tester, ())
        start_new_thread(force_tester, ())
        while True:
            pass
    #allows for keyboard interupt to work
    except KeyboardInterrupt:
        print("GOODBYE")
        return

startup()

