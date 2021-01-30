import os
import threading
from reddit_data_collection import *

#creates a timer event  and calls it periodically
def trigger_event():
    time = 60.0 * 5
    threading.Timer(time, trigger_event).start()
    os.system('clear')
    get_all_of_it()

try:
    trigger_event()
except Exception as ex:
    file = open('error.txt', 'w+')
    file.write('error caught: %s' % ex)
    file.close()
