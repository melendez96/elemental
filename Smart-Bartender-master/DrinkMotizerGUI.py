
#! /usr/bin/python
import time, threading
from Tkinter import *
import tkMessageBox
import ttk

import sys
import RPi.GPIO as GPIO
import json

#from dotstar import Adafruit_DotStar
#from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options

GPIO.setmode(GPIO.BCM)

FLOW_RATE = 0.6

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

        def menuItemClicked(self, drink_name):
                index = 0
                count = 0
                for d in drink_list:
                        if (d['name'] == drink_name):
                                index = count
                        count = count + 1
                                
                self.makeDrink(drink_name, drink_list[index]['ingredients'])
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

#bartender.buildMenu(drink_list, drink_options)
#bartender.run()


dgui = Tk()

#GPIO.cleanup()

#GUI Window Setup

#Sets main window size
dgui.title("")
dgui.attributes('-fullscreen', False)
dgui.geometry('650x650+100+50')
dgui.configure(background='black')


labelfont = ('times', 28, 'bold')
selectfont = ('times', 10, 'italic')
widget = Label(dgui, text='Elemental')
widget.config(font=labelfont)           
widget.config(height=3, width=20)       
widget.pack(expand=YES, fill=BOTH)
widget.place(x=310,y=-42)
widget.configure(background='black',foreground='white')


#Sets the size and position of the black background
menuframe = Canvas(dgui, width=550, height=800, bd=2, bg="black", relief=SUNKEN)
menuframe.pack(pady=(50,10), ipady=5, ipadx=0)

#Progress Bar
separator = Frame(dgui, height=30, width=800, bd=1)
separator.pack(padx=0, pady=4)
progressbarlabel = Label(separator, text='No comas ancias').pack(side="left")
progressbar = ttk.Progressbar(separator, orient=HORIZONTAL, length=400, mode='determinate')
progressbar.pack(side="left",padx=0, pady=0)


def settingsmenu():
     smenu = Toplevel()
     smenu.title('Settings')
     smenu.geometry('600x400+300+100')
     smenu.iconbitmap(bitmap='Drink.ico')
     
#Main
Drinkfont = ('times', 12, 'bold', 'italic')
ingredfont = ('times', 9)

basicMessage="Coloque un vaso, despues precione OK"
mojitoMessage="En el vaso, coloque 10 hojas de menta, 4 rodajas de limon ademas de 2 paquetes de azucar  hielo al gusto"

def Quit():
    GPIO.cleanup()
    dgui.destroy()

def ButtonPress():
     progressbar.start()
     
def Caipi():
    if tkMessageBox.askokcancel("Tequila Sunrise","Coloque 4 rodajas de limon ademas de un paquete de azucar en el vaso y mezcle"):
            bartender.menuItemClicked('drink')
            tkMessageBox.configure(background='black')

def SD():
    if tkMessageBox.askokcancel("Screwdriver",basicMessage):
            bartender.menuItemClicked('drink')
        

def RumCoke():
        bartender.menuItemClicked('Rum & Coke')
        

def VodkaTonic():
        bartender.menuItemClicked('Gin & Juice')
        

def Mojito():
    if tkMessageBox.askokcancel("Mojito",mojitoMessage):
            bartender.menuItemClicked('drink')
        

def CubaLibre():
    if tkMessageBox.askokcancel("Cuba Libre",basicMessage):
            bartender.menuItemClicked('drink')
        

def VodkaGimlet():
    if tkMessageBox.askokcancel("Vodka Gimlet",basicMessage):
            bartender.menuItemClicked('drink')
        

def VodkaShot():
    if tkMessageBox.askokcancel("Vodka Shot",basicMessage):
            bartender.menuItemClicked('drink')
        

def RumShot():
    if tkMessageBox.askokcancel("Rum Shot",basicMessage):
            bartender.menuItemClicked('drink')
        

def Cola():
    if tkMessageBox.askokcancel("Cola",basicMessage):
            bartender.menuItemClicked('drink')
        

def OJ():
    if tkMessageBox.askokcancel("Orange Juice",basicMessage):
            bartender.menuItemClicked('drink')
        
#Caipi Button

Caipib=Button(menuframe, justify = CENTER, bd=3,command=Caipi)
Caipipic = PhotoImage(file="teqsunrise.gif")
Caipib.config(image=Caipipic,width="130",height="130",compound=CENTER)
Caipib.config(text="Acapulqueando", font=Drinkfont)
Caipib.grid(row=0, column=0, padx=5, pady=5)
Caipiingred = Label(menuframe,text='Ron, limon & azucar',bg="black", fg='white').grid(row=1, column=0)

#SD Button

SDb=Button(menuframe, justify = CENTER, bd=3,command=SD)
SDpic = PhotoImage(file="screwdriver.gif")
SDb.config(image=SDpic, width="130",height="130",compound=CENTER)
SDb.config(text="Destornilladora", font=Drinkfont)
SDb.grid(row=0, column=1, padx=5, pady=5)
SDingred = Label(menuframe,text='Vodka & Jugo de Naranja',bg="black", fg='white').grid(row=1, column=1)

#Caipiroska button 

RCb=Button(menuframe, justify = CENTER, bd=3,command=ButtonPress, height=200)
RCpic = PhotoImage(file="whiterussian.gif")
RCb.config(image=RCpic,width="130",height="130",compound=CENTER)
RCb.config(text="Ruso Nevadon", font=Drinkfont)
RCb.grid(row=0, column=2, padx=5, pady=5)
RCingred = Label(menuframe,text='Vodka, Kaluha & Leche',bg="black", fg='white').grid(row=1, column=2)

#Rum and Coke Button

WCb=Button(menuframe, justify = CENTER, bd=3,command=RumCoke)
WCpic = PhotoImage(file="whiskeycoke.gif")
WCb.config(image=WCpic,width="130",height="130",compound=CENTER)
WCb.config(text="Ron con Coquita", font=Drinkfont)
WCb.grid(row=0,  column=3, padx=5, pady=5)
WCingred = Label(menuframe,text='Ron & Cola',bg="black", fg='white').grid(row=1, column=3)

#VS Button

VSb=Button(menuframe, justify = CENTER, bd=3,command=VodkaTonic)
VSpic = PhotoImage(file="vodkasprite.gif")
VSb.config(image=VSpic,width="130",height="130",compound=CENTER)
VSb.config(text="Vodka burbujeante", font=Drinkfont)
VSb.grid(row=2, column=0, padx=5, pady=5)
VSingred = Label(menuframe,text='Vodka & Agua Mineral',bg="black", fg='white').grid(row=3, column=0)

#GT Button

GTb=Button(menuframe, justify = CENTER, bd=3,command=ButtonPress)
GTpic = PhotoImage(file="gintonic.gif")
GTb.config(image=GTpic,width="130",height="130",compound=CENTER)
GTb.config(text="Ajas Mojito!", font=Drinkfont)
GTb.grid(row=2, column=1, padx=5, pady=5)
GTingred = Label(menuframe,text='Ginebra & Agua Tonica',bg="black", fg='white').grid(row=3, column=1)

#Cuba Libre Button

CLb=Button(menuframe, justify = CENTER, bd=3,command=ButtonPress)
CLpic = PhotoImage(file="longisland.gif")
CLb.config(image=CLpic,width="130",height="130",compound=CENTER)
CLb.config(text="Cuba Libre", font=Drinkfont)
CLb.grid(row=2, column=2, padx=5, pady=5)
CLingred = Label(menuframe,text='Ron, Cola & Limon',bg="black", fg='white').grid(row=3, column=2)

#VR Button

VRb=Button(menuframe, justify = CENTER, bd=3,command=ButtonPress)
VRpic = PhotoImage(file="vodkaRedbull.gif")
VRb.config(image=VRpic,width="130",height="130",compound=CENTER)
VRb.config(text="Vodka Volador", font=Drinkfont)
VRb.grid(row=2, column=3, padx=5, pady=5)
VRingred = Label(menuframe,text='Vodka & Redbull',bg="black", fg='white').grid(row=3, column=3)

#MH Button

MHb=Button(menuframe, justify = CENTER, bd=3,command=VodkaShot)
MHpic = PhotoImage(file="Manhattan.gif")
MHb.config(image=MHpic,width="130",height="130",compound=CENTER)
MHb.config(text="EL Shot", font=Drinkfont)
MHb.grid(row=4, column=0, padx=5, pady=5)
MHingred = Label(menuframe,text='Vodka',bg="black", fg='white').grid(row=5,column=0)

#CM Button

CMb=Button(menuframe, justify = CENTER, bd=3,command=RumShot)
CMpic = PhotoImage(file="Cosmo.gif")
CMb.config(image=CMpic,width="130",height="130",compound=CENTER)
CMb.config(text="Bebida de Pirata", font=Drinkfont)
CMb.grid(row=4, column=1, padx=5, pady=5)
CMingred = Label(menuframe,text='Ron',bg="black", fg='white').grid(row=5, column=1)

#CM Button

Colab=Button(menuframe, justify = CENTER, bd=3,command=Cola)
Colapic = PhotoImage(file="Cosmo.gif")
Colab.config(image=Colapic,width="130",height="130",compound=CENTER)
Colab.config(text="Coquita", font=Drinkfont)
Colab.grid(row=4, column=2, padx=5, pady=5)
Colaingred = Label(menuframe,text='Cola',bg="black", fg='white').grid(row=5, column=2)

#CM Button

OJb=Button(menuframe, justify = CENTER, bd=3,command=OJ)
OJpic = PhotoImage(file="Cosmo.gif")
OJb.config(image=OJpic,width="130",height="130",compound=CENTER)
OJb.config(text="Pa' los peques", font=Drinkfont)
OJb.grid(row=4, column=3, padx=5, pady=5)
OJingred = Label(menuframe,text='Jugo de Naranja',bg="black", fg='white').grid(row=5, column=3)

settingsbutton = Button(text = 'Opciones', height=2, width=10, command = settingsmenu).pack(side='right')
exitbutton = Button(text='No precionar', height=2, width=10, command=Quit).pack(side='right')

dgui.mainloop()
