#!/usr/bin/python2

import nxt.locator
from nxt.motor import *

turn = 200

def spin_around(b):
    m_back = Motor(b, PORT_A)
    m_back.turn(20, turn)

b = nxt.locator.find_one_brick()
spin_around(b)

