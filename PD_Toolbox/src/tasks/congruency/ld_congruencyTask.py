from __future__ import division

from psychopy import visual, core, event, logging
from ld_utils import createWindow, createOutputFile, getCircleColor
from ld_config import congruency_circleFillColor, congruency_circleRadius, congruency_circleLineColor, congruency_jitter
from ld_congruencyMenu import getParamMenu
from ld_messages import readyMessage
import numpy as np
from numpy import inf
from random import randint, uniform
import sys

task = sys.argv[1]

#Menu
infos = getParamMenu(task)

#Log
logging.addLevel(logging.EXP+1,'StartExp')
logging.addLevel(logging.EXP+2,'StartPerformance')
logging.addLevel(logging.EXP+4,'StartRest')
logging.addLevel(logging.EXP+5,'Key')
logging.addLevel(logging.EXP+6,'DisplayTarget')
logDat = logging.LogFile(createOutputFile('congruency', 'task', infos['subject']),
    filemode='w',  # if you set this to 'a' it will append instead of overwriting
    level=logging.EXP+1)  # errors, data and warnings will be sent to this logfile

#Create Window @TODO Check multiple monitor and flip
currWindow = createWindow(infos['fullScreen'])

#Create Mouse object but keep it invisible
m = event.Mouse(visible=False, win=currWindow)

#Create left circle
leftCircle = visual.Circle(currWindow, fillColor=congruency_circleFillColor, lineColor=congruency_circleLineColor, radius=congruency_circleRadius, edges=32, units='cm')
leftCircle.pos = (-congruency_circleRadius/2-5,0)

#Create right circle
rightCircle = visual.Circle(currWindow, fillColor=congruency_circleFillColor, lineColor=congruency_circleLineColor, radius=congruency_circleRadius, edges=32, units='cm')
rightCircle.pos = (congruency_circleRadius/2+5,0)

#Create grey line
#gLine = visual.Line(currWindow, start=(-1, -2/3), end=(1, -2/3), lineColor='grey')

#Create Right Box
#rightAnswer = visual.TextStim(currWindow, text='Right', pos=(.5, -5/6), color='gold')
#rightAnswer.setUnits = 'pixels'
#rightBox = visual.Rect(currWindow, width=rightAnswer.width/currWindow.size[0], height=rightAnswer.height+.01, pos=(.5, -5/6), lineColor='white')

#Create Left Box
#leftAnswer = visual.TextStim(currWindow, text='Left', pos=(-.5, -5/6), color='gold')
#leftAnswer.setUnits = 'pixels'
#leftBox = visual.Rect(currWindow, width=leftAnswer.width/currWindow.size[0] , height=leftAnswer.height+.01, pos=(-.5, -5/6), lineColor='white')

waitStim = visual.TextStim(currWindow, text=readyMessage[infos['language']], color='gold',wrapWidth=100, pos=(0,-.7))
waitStim.draw()
currWindow.flip()

out = event.waitKeys(maxWait=np.inf, keyList=['5'], timeStamped=True)

#Reset Clock
globalClock = core.Clock()  
logging.setDefaultClock(globalClock)

# Draw everything 
#leftBox.draw()
#rightBox.draw()
#gLine.draw()
#leftAnswer.draw()
#rightAnswer.draw()
leftCircle.draw()
rightCircle.draw()

currWindow.flip(clearBuffer=False)

core.wait(infos['durRest'])

nBlock = 0
nextBlock = True
for nKey in infos['design']:
    if nKey[0]>1:
        currWindow.logOnFlip(str(nBlock), level=logging.EXP+4)
        nBlock += 1
        leftCircle.fillColor = congruency_circleFillColor
        rightCircle.fillColor = congruency_circleFillColor
        leftCircle.draw()
        rightCircle.draw()
        currWindow.flip(clearBuffer=False)
        nextBlock = True
        core.wait(infos['durRest'])
    else:
        leftCircle.fillColor, rightCircle.fillColor = getCircleColor(nKey)
        #StartPerformance
        if nextBlock:
            currWindow.logOnFlip(str(nBlock), level=logging.EXP+2)           
            nextBlock = False
        
        leftCircle.draw()
        rightCircle.draw()
        currWindow.logOnFlip('', level=logging.EXP+6)
        currWindow.flip(clearBuffer=False)

        currKey = event.waitKeys(maxWait=inf, keyList=['1','2','3','4','escape'])
		
			#if m.isPressedIn(leftBox):
            #    currWindow.logOnFlip('left', level=logging.EXP+6)
            #    next=True
            #if m.isPressedIn(rightBox):
            #    currWindow.logOnFlip('right', level=logging.EXP+6)
            #    next=True
        
		    # Check if escape have been pressed
        if 'escape' in currKey:
        	logging.flush()
        	core.quit()		  
				  
        leftCircle.fillColor = congruency_circleFillColor
        rightCircle.fillColor = congruency_circleFillColor
        leftCircle.draw()
        rightCircle.draw()
        currWindow.flip(clearBuffer=False)
        core.wait(uniform(congruency_jitter[0],congruency_jitter[1]))

leftCircle.fillColor = congruency_circleFillColor
rightCircle.fillColor = congruency_circleFillColor
leftCircle.draw()
rightCircle.draw()
currWindow.flip(clearBuffer=False)
core.wait(infos['durRest'])    

currWindow.close()
