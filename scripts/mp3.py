import os
import time
import RPi.GPIO as GPIO
import random 
import subprocess 
import logging


RPI_GPIO_EXISTS = True

# Predefine variables
BUTTONS_PINS = [26]
BUTTONS_MODE = "pull_down"
BUTTON_IS_ACTIVE = 1
MP3_DIR = "/home/pi/workspace/TouchSelfie-extended/mp3/"

try:
    import RPi.GPIO as GPIO
    ## GPIO pin definition for hardware buttons
    BUTTONS_PINS = [26]    
    BUTTON_IS_ACTIVE = 1         # active 1 GPIO (pull_down with switch to VDD)
except ImportError:
    RPI_GPIO_EXISTS = False

logger = logging.getLogger('mp3')
logger.setLevel('DEBUG')
stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stderr_log_handler.setFormatter(formatter)


class Buttons():
    """Hardware Buttons wrapper class"""

    def __init__(self, buttons_pins=BUTTONS_PINS, mode=BUTTONS_MODE, active_state=BUTTON_IS_ACTIVE):
        """Constructor for Buttons

        Arguments:
            button_pins [list(int)]         : list of GPIO pins
            mode ["pull_up" or "pull_down"] : the pull state of the GPIO
            active_state [0 or 1]           : GPIO status when activated

        Note: this is safe to use this class on systems that don't have GPIO module
            in this case, has_buttons() methods returns False
        """
        self.buttons_pins = buttons_pins
        logger.info("Pins configured " + str(self.buttons_pins))
        self.active_state = active_state
        self._has_buttons = False
        if RPI_GPIO_EXISTS:
            if mode == "pull_up":
                self.mode = GPIO.PUD_UP
            elif mode == "pull_down":
                self.mode = GPIO.PUD_DOWN
            else:
                raise ValueError("Unknown pull_up_down mode %s"%mode)
                
            GPIO.setmode(GPIO.BCM)
            logger.info("Setup Pins")
            
            for pin in self.buttons_pins:
            	logger.info("Setup Pin %d" % pin)
                GPIO.setup(pin, GPIO.IN, pull_up_down = self.mode)
            if len(buttons_pins) != 0:
                self._has_buttons = True
            else:
                self._has_buttons = False

    def __del__(self):
        """Cleanup GPIO"""
        if self._has_buttons:
            GPIO.cleanup()

    def has_buttons(self):
        """Wether buttons were configured

        returns: True if at lease one button configured
        """
        return self._has_buttons

    def buttons_number(self):
        """Number of configured hardware buttons

        returns: the number of buttons configured
        """
        return len(self.buttons_pins)

    def state(self):
        """Current state of the hardware buttons

        buttons are checked in the order provided to the constructor
        as soon as a button state == active_state, the loop ends and the
        index of the active button is returned (first items of the buttons list
        therefore have higher priority)

        returns:
            0 if no button currently active
            i (i>0) the index of the first active button with:
                i=1 => button_pins[0] is active
                i=2 => button_pins[1] is active
                ...
        """
        if not self._has_buttons:
            return 0

        for i,pin in enumerate(self.buttons_pins,1):
            if GPIO.input(pin) == self.active_state:
                return i
        else :
            # reached the end of pins, none active
            return 0


if __name__ == '__main__':
    import time
    import sys
    buttons = Buttons()
    last = 0
    proc = None
    
    if buttons.has_buttons():
        print "Press hardware buttons to see change, ctrl+C to exit"
    else:
        print "No button configured (no access to GPIO or empty button list)"
        print "Number of buttons is %d" % buttons.buttons_number()
        sys.exit()
	
    while True:
        state = buttons.state()
			        
        if last != state:
            print "new state: %d"%state
            if state == 1:
            		if proc != None & proc.poll() != 0:
            			logger.info("Kill process")
            			logger.info("Process state " + str( proc.poll() ))
            			subprocess.call(['killall', '/usr/bin/omxplayer.bin'])
            			
            		randomfile = random.choice(os.listdir(MP3_DIR))
            		mp3file =  MP3_DIR +  randomfile
            		logger.info("Playing: " + mp3file)
            		proc = subprocess.Popen (['omxplayer', '-o' 'local', mp3file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, preexec_fn=os.setsid)			            		
            		
            last = state
        time.sleep(0.1)
        

	