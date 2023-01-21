from TempSensor import *
from do_connect import *
import time

while True:
    connect()
    tempsensor()
    putFile()