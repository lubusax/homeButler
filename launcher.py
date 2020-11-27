#! /usr/bin/python3.7
import os
import time

from dicts.ras_dic import PinsBuzzer
#from dicts.ras_dic import PinsDown
#from dicts.ras_dic import PinsOK

from lib import Display
#from lib import CardReader
from lib import PasBuz
#from lib import Button
#from lib import Tasks
#from lib import Utils

#import traceback
#from io import StringIO


#Utils.initializeDevice()

Buzz = PasBuz.PasBuz(PinsBuzzer)
Disp = Display.Display()
#Reader = CardReader.CardReader()
#B_Down = Button.Button(PinsDown)
#B_OK = Button.Button(PinsOK)
#Hardware = [Buzz, Disp, Reader, B_Down, B_OK]
 
#Tasks = Tasks.Tasks(Hardware)

def mainLoop():
  try:
    Buzz.Play("cardswiped")
    Disp.displayGreetings()
    
    # while True:
    #   pass
  except Exception as e:
    print("Exception : ", e)

mainLoop()
