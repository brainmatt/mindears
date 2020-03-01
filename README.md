# MindEars
A wearable robot imitating animal ears controlled by brainwaves collected by a Muse 2 device

## Introduction
This is one of my fun projects regarding brain-computer interfaces.

It is based on:
- a "Muse 2" device providing access to EEG data from your own brain
- the "Mind Monitor" Android App receiving the EEG data from the Muse device and streaming it to a Computer
- the here provided "MindEars" server and client code
- a wearable Lego robot built from the "Lego Mindstorm NXT" kit
	-> this Lego robot is a head-mounted wearable device which imitates "animal ears".

Ears of certain animals (e.g. cats and dogs) displaying their state of mood.
e.g. when a Cat is attracted by something than it points its ears. When it is relaxed it put on their ears.
In the same way the "wearable animal ears" robot is working. It provides a direct view of the internal mind state and mood of the person wearing those "artificially animal ears". The robot is driven by 3 different mind states (active/neutral/silent) which are gathered on behalf of the absolute "alpha wave" values - the amount of Alpha waves are one of the indicators for a "meditation" state. According to dynamic calculated limits the implemented state machine drives the ears front, mid or back in real-time. Additionally it gathers the "eye blinking" from captured EEG data and uses "2 fast blinks" as a signal for bending and unbending the ears (point ears and  put on ears).


## Features
- threaded UDP server to receive EEG data from the "Mind Monitor" app
- automatic calibration to seamlessly adapt to any brain
- calculation of alpha wave averages and dynamic mind state limits
- serialization and queuing of the ear commands to the mindear-client
- interfacing with the Lego NXT brick to send direct motor commands in real-time
- EEG and Blink callbacks for analyzing the data stream


## Muse 2 brain sensing headband:
Muse is a wearable brain sensing headband. The device measures brain activity via 4 electroencephalography (EEG) sensors. An accompanying mobile app converts the EEG signal into audio feedback that is fed to the user via headphones.
The device operates by representing brain waves that correspond to a more relaxed state through the sound of tweeting birds, and higher amounts of brain activity is represented by storm sounds. It was demonstrated that Muse can be used for ERP research, with the advantage of it being low cost and quick to setup. Specifically, it can easily quantify N200, P300, and reward positivity. It is also widely used for a wide variety of other applications ranging from health and wellbeing to scientific and medical research. It is claimed that using the headband helps in reaching a deep relaxed state. Muse is worn over the ears and connects to a companion mobile app via bluetooth. The use of Muse enables the use of biofeedback.
(this paragraph is based on Wikipedia)


## Mind Monitor App
The "Mind Monitor" app is a must-have thirdparty add-on app for the Muse headband. It directly connects to the Muse 2 headband and provides raw EEG data plus pre-calculated amounts of alpha/beta/theta/delta/gamma waves plus eye blink detection. For this project it is used as the proxy for gathering the raw data from the headband and streaming them to a computer running the mindear-server/client.


## MuseLSL
My first approach was re-implementing and adapting MuseLSL (please see Url below) which provides direct access the Muse device from a computer but missing the pre-calulated wave frequency and eye blink detection. Also I successfully implemented the brainwave frequency calculation using Fast Fourier Transformation before I happily found the ready-implemented neurofeedback example included in the MuseLSL distribution. Anyway especially for bending/unbending the ears I planned to use the eye blink detection as an additional trigger next to the moving ears front and back.


## MindEars server:
The server receives the EEG data (only the alpha waves) from the Mind Monitor via an standard OSC stream (the specifications of this stream are availble on the Mind Monitor website - see Urls below). It smootes the data by calculating the averages of sequences of 50 samples to avoid any jumps. It also calculates the overall average of all received alpha wave data to re-calculate the dynamic limits of its state machine. For all changes of the brain state (e.g. from active to neutral) it queues commands to the mindear-client.
It also automatically starts the mindear-client as a sub-process. Both process are connected and serialized by a simple file-based built-in queuing system.

Required python modules (install with pip3 in a python3 based python virtualenv)
- pythonosc (python3 only)
- os
- sys
- time
- logging
- argparse
- subprocess


## MindEars client:
The client is attached to the command queue provided by the mindear-server. It gathers the queued commands and send them as direct mo
tor commands to the Lego NXT brick which is driving the 2 seperated motors of the robot (Motor A for moving the ears, Motor B for bending/unbending the ears).

Required python modules (install with OS packages)
- python-nxt (python2 only)
- python-sh 


## Background
 At some point in life I started to realize that the human brain is our main and only device which connects us to the so called "reality". I also found out that the brain not only connects to our biological "sensors" (e.g. eyes for vision, skin for touch etc.) but it also "flavors" the data which is being read according to experiences from the past, current thoughts and current feelings.

From those 2 facts one can derive that there is no "objective view" of our the "reality" but only "subjective expressions" which are the result of our human sensor data coupled with our subjective "flavor" - so each human actually experiences her own subjective reality!

Next thing which came into my mind:
If I am part of forming my own subjective reality it would be useful to understand how this additional "flavoring" of the reality in my brain is working.

... so I recently started to setup my personal Electroencephalography laboratory (EEG) using the "Muse 2" brain sensing device. After exploring this gadget a bit it allowed me to stream my brainwave data in real-time to either a smartphone app or directly to a PC for further analytics. Additional to that the "Muse 2" comes with an awesome meditation app which actually discovers when loosing focus within the meditation in real-time. It then gives a soft audio signal to return the focus.


## Urls:
- Muse 2 - brainwave headband - https://choosemuse.com/muse-2/
- Muse Wikipedia - https://en.wikipedia.org/wiki/Muse_(headband)
- Mind Monitor - awesome thirdparty app for Muse - https://mind-monitor.com/
- MuseLSL - great tool to stream Muse EEG data directly to a PC - https://github.com/alexandrebarachant/muse-lsl
- MindEars - this project github repository - https://github.com/brainmatt/mindears/
- Lego NXT - a robotic kit made by Lego - https://en.wikipedia.org/wiki/Lego_Mindstorms_NXT


## Dislaimer:
I am not affiliated with any of the here named companies and just doing this for my own fun.
The  idea for this project is slightly inspired by a now deprecated product called "Necomimi"





