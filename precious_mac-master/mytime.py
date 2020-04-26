from datetime import datetime
import time
today = datetime.fromtimestamp(time.time()-3600) # hour earlier
print today
today = datetime.fromtimestamp(time.time()) # hour earlier
print today

from threading import Timer

def print_time():
    print "From print_time", time.time()

Timer(5, print_time, ()).start()
time.sleep(11)  # sleep while time-delay events execute