from sensors import lese_sensor
from time import sleep
from gpiozero import LED
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import threading

class BackgroundThread(threading.Thread):
    wanted_list = {"Chemie", "Deutsch", "Mathe"}
    current_list = {"Chemie"}
    led_gruen = None
    led_gelb = None
    led_rot = None
    gelb_leuchtet = False
    
    def reset(self):
        self.current_list = set()

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    def startup(self) -> None:
        """
    Method that is called before the thread starts.
    Initialize all necessary resources here.
    :return: None
    """
        self.led_gruen = LED("BOARD37")
        self.led_rot = LED("BOARD36")
        self.led_gelb = LED("BOARD33")
        return

    def shutdown(self) -> None:
        """
    Method that is called shortly after stop() method was called.
    Use it to clean up all resources before thread stops.
    :return: None
    """
        GPIO.cleanup()

    def handle(self) -> None:
        """
    Method that should contain business logic of the thread.
    Will be executed in the loop until stop() method is called.
    Must not block for a long time.
    :return: None
    """
        item = lese_sensor()
        if item:
            item = item.strip()
            # print(item)
            if item not in self.wanted_list:
                led_kurz_leuchten_lassen(self.led_rot)
            else:
                if item not in self.current_list:
                    self.current_list.add(item)
                    led_kurz_leuchten_lassen(self.led_gruen)
                else:
                    self.current_list.remove(item)
                    led_kurz_leuchten_lassen(self.led_rot)
        if self.current_list == self.wanted_list:
            if self.gelb_leuchtet:
                self.led_gelb.off()
                self.gelb_leuchtet = False
        else:
            if not self.gelb_leuchtet:
                self.led_gelb.on()
                self.gelb_leuchtet = True

    def run(self) -> None:
        """
    This method will be executed in a separate thread
    when start() method is called.
    :return: None
    """
        self.startup()
        while not self._stopped():
            self.handle()
        self.shutdown()


def led_kurz_leuchten_lassen(led, zeit=1):
    # IN NEUEM THREAD
    led.on()
    sleep(zeit)
    led.off()

if __name__ == "__main__":
    led_gruen = LED("BOARD37")
    led_rot = LED("BOARD36")
    led_gelb = LED("BOARD33")
    
    led_gruen.on()
    led_rot.on()
    led_gelb.on()

    while True:
        pass
