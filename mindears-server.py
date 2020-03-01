#!/usr/bin/env python
# runs only in python3 
import os
import sys
import time
import logging
import argparse
import subprocess
from pythonosc import dispatcher
from pythonosc import osc_server

# from https://mind-monitor.com/forums/viewtopic.php?t=858

currentpath = os.path.dirname(os.path.realpath(sys.argv[0]))
logging.basicConfig(filename=currentpath + '/mindears.log',level=logging.INFO)

# 0 = activ, 1 = neutral, 2 = silent
brainstate = 1
brainstate_last = 1
# lower and upper limit
MEDITATION_NEUTRAL = 50
MEDITATION_SILENT = 60

# autocalibration limits
AUTOCALIBRATION_ACTIVE_LIMIT = 5
AUTOCALIBRATION_SILENT_LIMIT = 5

# calibration method
calibration_method = "auto"
# requiered samples to switch to autocalibration
calibration_switch = 200

# sum of captured alpha wave samples within one calibration_sequence
alphasamples = 0

# global sum of all captured alpha wave samples
alphasamples_sum = 0
# global count of all alpha wave samples
alphasamples_count = 0

# ignore the first pack of messages for calibration
CALIBRATION = 50
calibration_sequence = 0

# current state of the ears, 0 = normal, 1 = bend
earstate = 0

# blinks
blinks = 0

# last blink timestamp
lastblink = 0
blinkinterval = 1

# brain command queue
braincmds = currentpath + '/braincmds.txt'


def braincmd(cmd):
    with open(braincmds, 'a') as out:
        out.write(cmd + '\n')

def braincmdreset():
    with open(braincmds, 'w') as out:
        out.truncate()

def eeg_handler(unused_addr,ch1,ch2,ch3,ch4,ch5,ch6):
    print("EEG per channel: ",ch1,ch2,ch3,ch4,ch5,ch6)
    

def alpha_handler(unused_addr,ch1,ch2):
    #print("Alpha absolute: ",ch1,ch2)
    global brainstate
    global brainstate_last
    global MEDITATION_SILENT
    global MEDITATION_NEUTRAL
    global CALIBRATION
    global calibration_sequence
    global currentpath
    global alphasamples
    global alphasamples_count
    global alphasamples_sum
    global calibration_method
    global calibration_switch

    # capture samples
    calibration_sequence = calibration_sequence + 1
    # capture global count of all samples
    alphasamples_count = alphasamples_count + 1
    # capture gobal sum of all samples
    alphasamples_sum = alphasamples_sum + ch2
    if calibration_sequence < CALIBRATION:
        alphasamples = alphasamples + ch2
        #print("Calibration - capturing samples - " + str(ch2) + " / " + str(alphasamples))
        return

    # reset calibration_sequence
    calibration_sequence = 0
    # add last sample in calibration
    alphasamples = alphasamples + ch2
    # calculate sum/count*100
    alphawaves = alphasamples/CALIBRATION*100
    # reset alphasamples
    alphasamples = 0
    # calulate global sum/count
    alphawaves_global = alphasamples_sum/alphasamples_count
    
    # which callibration method ? - needs at least alphasamples_count samples
    if calibration_method == "auto" and alphasamples_count > calibration_switch:
        alphawaves_global_average = alphawaves_global*100
        MEDITATION_NEUTRAL = alphawaves_global_average - AUTOCALIBRATION_ACTIVE_LIMIT
        MEDITATION_SILENT = alphawaves_global_average + AUTOCALIBRATION_SILENT_LIMIT
        #logging.info('MINDEARSERVER: switching to autocalibration using dynamic limits')

    #print('--> Alpha Relaxation: ' + str(alphawaves))
    if alphawaves > MEDITATION_SILENT:
        brainstate = 2
    elif alphawaves > MEDITATION_NEUTRAL and alphawaves < MEDITATION_SILENT:
        brainstate = 1
    elif alphawaves < 0:
        brainstate = 2
    elif alphawaves < MEDITATION_NEUTRAL:
        brainstate = 0

    print('Alpha Relaxation: ' + str(alphawaves) + " average: " + str(alphawaves_global) + "\n  MEDITATION_NEUTRAL: " + str(MEDITATION_NEUTRAL) + " MEDITATION_SILENT: " + str(MEDITATION_SILENT) + "\n  brainstate: " + str(brainstate) + " brainstate_last: " + str(brainstate_last))
    if brainstate_last != brainstate:
        if brainstate == 0 and brainstate_last == 1:
            #print("turning to active - from neutral - front")
            logging.info('MINDEARSERVER: turning to active - from neutral - front')
            braincmd('front')
        elif brainstate == 0 and brainstate_last == 2:
            #print("turning to active - from silent - front+front")
            logging.info('MINDEARSERVER: turning to active - from silent - front+front')
            braincmd('frontfront')

        elif brainstate == 1 and brainstate_last == 0:
                #print("turning to neutral - from active - back")
                logging.info('MINDEARSERVER: turning to neutral - from active - back')
                braincmd('back')
        elif brainstate == 1 and brainstate_last == 2:
                #print("turning to neutral - from silent - front")
                logging.info('MINDEARSERVER: turning to neutral - from silent - front')
                braincmd('front')

        elif brainstate == 2 and brainstate_last == 1:
            #print("turning to silent from neutral - back")
            logging.info('MINDEARSERVER: turning to silent from neutral - back')
            braincmd('back')
        elif brainstate == 2 and brainstate_last == 0:
            #print("turning to silent from active - backback")
            logging.info('MINDEARSERVER: turning to silent from active - backback')
            braincmd('backback')

        brainstate_last = brainstate


def blink_handler(unused_addr,ch1,ch2):
    print("Blink: ",ch1,ch2)
    global earstate
    global blinks
    global lastblink
    global blinkinterval
    global currentpath

    # check if we blink more than once in the given blinkinterval
    if blinks > 0:
        ts = time.time()
        #print("lastblink = " + str(lastblink) + " ts = " + str(ts) + " lastblink = " + str(lastblink))
        if (ts - lastblink) < blinkinterval:
            print("!! blinked 2. time within " + str(blinkinterval) + "s")

            # check the earstate
            if earstate == 0:
                # bend
                #print("bending ears - on")
                logging.info('MINDEARSERVER: bending ears')
                braincmd('bend')
                earstate = 1
            else:
                # unbend
                #print("unbending ears - off")
                logging.info('MINDEARSERVER: unbending ears')
                braincmd('unbend')
                earstate = 0

            blinks = 0
    else:
        print("setting blinks = 1")
        blinks = 1

    lastblink = time.time()



if __name__ == '__main__':
    port = 5000
    ip = "192.168.88.109"
    calibration_method = "auto"
    auto_start_mindears_client = True
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="local ip address to run the mindears-server on")
    parser.add_argument("-p", "--port", help="local port to run the mindears-server on")
    parser.add_argument("-c", "--calibration", help="static/auto - static vs automatic/dynamic calibration (default 'auto')")
    parser.add_argument("-m", "--mindearsclient", help="true/false - automatic start the mindears-client (default 'true')")
    args = vars(parser.parse_args())

    if not args['ip']:
        logging.info('MINDEARSERVER: no ip given, using default ip: ' + str(ip))
    else:
        ip = args['ip']
        logging.info('MINDEARSERVER: ip given, using default ip: ' + str(ip))

    if not args['port']:
        logging.info('MINDEARSERVER: no port given using default port: ' + str(port))
    else:
        port = args['port']
        logging.info('MINDEARSERVER: port given, using port: ' + str(port))

    if not args['calibration']:
        logging.info('MINDEARSERVER: no calibration method given using default method: ' + str(calibration_method))
    else:
        calibration_method = args['calibration']
        logging.info('MINDEARSERVER: calibration method given, using method: ' + str(calibration_method))

    if not args['mindearsclient']:
        logging.info('MINDEARSERVER: no configuration given to autostart the mindears-client (default true)')
    elif args['mindearsclient'] == "false":
        auto_start_mindears_client = False
        logging.info('MINDEARSERVER: configuration given to not start the mindears-client')


    logging.info('MINDEARSERVER: starting mindears-server')

    logging.info('MINDEARSERVER: resetting braincmds - ' + braincmds)
    braincmdreset()

    if auto_start_mindears_client:
        logging.info('MINDEARSERVER: starting mindears-client')
        mc = subprocess.Popen([ currentpath + "/mindears-client.py"])

    logging.info('MINDEARSERVER: initialyze dispatcher')
    # http://forum.choosemuse.com/t/muse-direct-osc-stream-to-python-osc-on-win10/3506/2
    dispatcher = dispatcher.Dispatcher()
    #dispatcher.map("/muse/eeg", eeg_handler, "EEG")
    dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, "EEG")
    dispatcher.map("/muse/elements/blink", blink_handler, "EEG")

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    logging.info("MINDEARSERVER: serving on {}".format(server.server_address))
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        if auto_start_mindears_client:
            logging.info('MINDEARSERVER: stopping mindears-client')
            mc.kill()
        logging.info('MINDEARSERVER: stopping mindears-server')



