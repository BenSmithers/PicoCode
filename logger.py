import os 
from time import time 
import sys 

logfile = "log.txt"

fullpath = os.path.join(os.path.dirname(__file__), logfile)

message = " ".join(sys.argv[1:])

with open(fullpath, 'a') as _obj:
    _obj.write("{} - {}\n".format(time(), message))
