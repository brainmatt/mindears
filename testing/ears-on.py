#!/usr/bin/python2

import nxt.locator
from nxt.motor import *

turn = 1000

def spin_around(b):
    m_ears_off = Motor(b, PORT_B)
    m_ears_off.turn(50, turn)

b = nxt.locator.find_one_brick()
spin_around(b)

