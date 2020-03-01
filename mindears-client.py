#!/usr/bin/python2

import os
import sys
import time
import logging
import nxt.locator
# from python-nxt
from nxt.motor import *
# from python-sh
from sh import sed

singlestep = 200
doublestep = 2 * singlestep
front = -20
back = 20
benddegrees = 1000
earson = 50
earsoff = -50

currentpath = os.path.dirname(os.path.realpath(sys.argv[0]))
logging.basicConfig(filename=currentpath + '/mindears.log',level=logging.INFO)
braincmds = currentpath + '/braincmds.txt'
cmddelay = 2

def drive_motor(motor, degrees, speed):
    motor.turn(speed, degrees)

# main loop
logging.info('MINDEARCLIENT: Entering the main loop')
brick = nxt.locator.find_one_brick()
logging.info('MINDEARCLIENT: connected Lego NXT brick')

while(True):
    first_cmd = ""
    with open(braincmds) as f:
        first_cmd = f.readline()
        first_cmd = first_cmd.strip("\n\r")
    if first_cmd != "":
        #logging.info('MINDEARCLIENT: running cmd: ' + first_cmd)
        motorA = Motor(brick, PORT_A)
        motorB = Motor(brick, PORT_B)
        if first_cmd == "front":
            logging.info('MINDEARCLIENT: running cmd front')
            drive_motor(motorA, singlestep, front)
        elif first_cmd == "back":
            logging.info('MINDEARCLIENT: running cmd back')
            drive_motor(motorA, singlestep, back)
        if first_cmd == "frontfront":
            logging.info('MINDEARCLIENT: running cmd frontfront')
            drive_motor(motorA, doublestep, front)
        elif first_cmd == "backback":
            logging.info('MINDEARCLIENT: running cmd backback')
            drive_motor(motorA, doublestep, back)
        if first_cmd == "bend":
            logging.info('MINDEARCLIENT: running cmd bend')
            drive_motor(motorB, benddegrees, earson)
        elif first_cmd == "unbend":
            logging.info('MINDEARCLIENT: running cmd unbend')
            drive_motor(motorB, benddegrees, earsoff)
        sed(['-i', '1d', braincmds])

    time.sleep(cmddelay)





