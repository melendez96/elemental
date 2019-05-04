import time
import sys
import RPi.GPIO as GPIO
import json
import threading

#from dotstar import Adafruit_DotStar
#from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options

GPIO.setmode(GPIO.BCM)

FLOW_RATE = 600.0/1000.0

class Bartender(): 
        def __init__(self):
                self.running = False
                
                # load the pump configuration from file
                self.pump_configuration = Bartender.readPumpConfiguration()
                for pump in self.pump_configuration.keys():
                        #print(self.pump_configuration[pump]['pin'])
                        GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH) 

                print "Done initializing"

        @staticmethod
        def readPumpConfiguration():
                return json.load(open('pump_config.json'))

        def menuItemClicked(self, menuItem):
                if (menuItem == "drink"):
                        self.makeDrink('Rum & Coke', drink_list[0]['ingredients'])
                        return True
        
        def pour(self, pin, waitTime):
                GPIO.output(pin, GPIO.LOW)
                time.sleep(waitTime)
                GPIO.output(pin, GPIO.HIGH)

        def makeDrink(self, drink, ingredients):
                # cancel any button presses while the drink is being made
                self.running = True

                # Parse the drink ingredients and spawn threads for pumps
                maxTime = 0
                pumpThreads = []
                
                for ing in ingredients.keys():
                        for pump in self.pump_configuration.keys():
                                if ing == self.pump_configuration[pump]["value"]:
                                        waitTime = ingredients[ing] * FLOW_RATE
                                        #print(waitTime)
                                        if (waitTime > maxTime):
                                                maxTime = waitTime
                                        pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
                                        pumpThreads.append(pump_t)

                # start the pump threads
                for thread in pumpThreads:
                        thread.start()

                # wait for threads to finish
                for thread in pumpThreads:
                        thread.join()

                # sleep for a couple seconds to make sure the interrupts don't get triggered
                time.sleep(2);

                # reenable interrupts
                # self.startInterrupts()
                self.running = False

bartender = Bartender()
bartender.menuItemClicked('drink')
#bartender.buildMenu(drink_list, drink_options)
#bartender.run()




