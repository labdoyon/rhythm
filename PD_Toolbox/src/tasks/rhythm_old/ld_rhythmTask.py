# -*- coding: utf-8 -*-
from __future__ import division
from psychopy import visual, core, event, logging, sound
from ld_utils import createWindow, createOutputFile
from numpy import inf
from ld_messages import readyMessage
from ld_rhythmMenu import getParamMenu
import numpy as np
import sys

print 'Using %s(with %s) for sounds' % (sound.audioLib, sound.audioDriver)

#Menu
infos = getParamMenu()

#Log
logging.addLevel(logging.EXP+1,'StartExp')
logging.addLevel(logging.EXP+2,'StartPerformance')
logging.addLevel(logging.EXP+4,'StartRest')
logDat = logging.LogFile(createOutputFile(),
    filemode='w',  # if you set this to 'a' it will append instead of overwriting
    level=logging.DEBUG)  # errors, data and warnings will be sent to this logfile

#Create Window @TODO Check multiple monitor and flip
currWindow = createWindow()

# Create Sound
tone = sound.Sound('F', octave=5, sampleRate=44100, secs=0.050)

# Create Cross before starting the experiment 
cross = visual.ShapeStim(currWindow, units='cm',
    vertices=((0, -2), (0, 2), (0,0), (-2,0), (2, 0)),
    lineWidth=900,
    closeShape=False,
    lineColor='red')

waitStim = visual.TextStim(currWindow, text=readyMessage[infos['language']], color='gold',wrapWidth=100, pos=(0,0))

waitStim.draw()
currWindow.flip()

# Wait for trigger
out = event.waitKeys(maxWait=inf, keyList=['5'], timeStamped=True)

# Reset Clock
globalClock = core.Clock()
logging.setDefaultClock(globalClock)

#First RED Cross
currWindow.logOnFlip('', level=logging.EXP+1)
cross.draw()
currWindow.flip()
core.wait(infos['durRest'])

nbBlock = 0

while nbBlock <= infos['nbBlocks']:
    currWindow.logOnFlip('', level=logging.EXP+2)
    cross.setLineColor('green')
    cross.draw()
    currWindow.flip()
    startBlock = core.getTime()

    nbip = 0
    while core.getTime() < startBlock + infos['halfBlockDuration']:
        if nbip > 21:
            #Play sound
            tone.play()
            #Hide Cross and wait .5s 
            cross.setLineColor('black')
            cross.draw()
            currWindow.flip()
            core.wait(.5)
            
            #Show green Cross and wait infos['freq']-.5s
            cross.setLineColor('green')
            cross.draw()
            currWindow.flip()
            core.wait(infos['freq']-.5)
        else:
            #Play sound
            tone.play()
            core.wait(infos['freq']-0.001)
            nbip +=1
        
    logging.flush()
    core.wait(infos['halfBlockDuration'])
    currWindow.logOnFlip(str(nbBlock), level=logging.EXP+4)
    cross.setLineColor('red')
    cross.draw()
    currWindow.flip()   
    core.wait(infos['durRest'])
    nbBlock += 1