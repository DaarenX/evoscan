import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522
from time import sleep
from datetime import datetime, timedelta


class PatchedSimpleMFRC522(SimpleMFRC522):
    def __init__(self, **kwargs):
        self.READER = MFRC522(**kwargs)


letzteID = None
zeitpunkt = datetime(2000, 1, 1, 0, 0, 0)
wartezeit = timedelta(seconds = 5)

reader = PatchedSimpleMFRC522(bus=0, pin_rst=22)
reader2 = PatchedSimpleMFRC522(bus=1, pin_rst=16)



def ueberschneiden():
    id, text = reader.read_no_block()
    if not id:
       id, text = reader2.read_no_block() 
    return id, text

def lese_sensor():
    global zeitpunkt
    global letzteID
    global wartezeit
    id, text = ueberschneiden()
    zeit = datetime.now()
    if (zeit - zeitpunkt) < wartezeit and id == letzteID:
        id = None
        text = None
    elif id:
        letzteID = id
        zeitpunkt = zeit
    return text
        

if __name__ == "__main__":
    try:
        while True:
            # id, text =  ueberschneiden()
            # if id:
            #     print(id, text)
            
            text = input('New data:')
            print("Now place your tag to write")
            reader.write(text)
            print("Written")
    finally:
        GPIO.cleanup()



