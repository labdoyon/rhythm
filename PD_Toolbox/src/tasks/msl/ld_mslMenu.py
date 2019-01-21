# ABore - 6 Avril 2017
# CRIUGM
# -*- coding: utf-8 -*-

from psychopy import gui  #fetch default gui handler (qt if available)
import Tkinter

import os
import sys
from ld_config import msl_seqA, msl_seqB, msl_nbBlocks, msl_nbKeys, msl_nbSeqIntro, msl_durRest, observers, output, subjectPrefix, fullScreen, flipMonitor
import numpy as np
import time
import json

def getParamMenu(currTask):
    # create a DlgFromDict
    info = {'Observer':observers,
        'seq':[' - '.join(map(str, msl_seqA)), ' - '.join(map(str, msl_seqB))],
        'nbBlocks':msl_nbBlocks,
        'nbKeys':msl_nbKeys,
		'hand': ['left','right'],
        'introNbSeq':msl_nbSeqIntro,
        'durRest':msl_durRest,
        'language':['French', 'English'],
        'flipMonitor':flipMonitor,
        'fullScreen':fullScreen,
		'subject':subjectPrefix}
    
    infoDlg = gui.DlgFromDict(dictionary=info, title='Stim Experiment - v0.1',
        order=['Observer','subject','hand', 'language','flipMonitor','fullScreen','seq','nbBlocks','nbKeys','introNbSeq','durRest'],
        tip={'Observer': 'trained visual observer, initials', 'durRest': 'seconds', 'flipMonitor':'Doesnt work yet'})

    if infoDlg.OK:  # this will be True (user hit OK) or False (cancelled)
        info['language'] = checkLanguage(info['language'])
        json.dump(info, open(os.path.join(output,'msl',info['subject']+'_'+currTask+'_'+time.strftime("%Y%m%d-%H%M%S")+'.cfg'),'a+'))
        return info
    else:
		sys.exit("Cancel MSL")
		
def checkLanguage(currLanguage):
    if currLanguage == 'French': 
        return 0
    elif currLanguage == 'English':
        return 1

# Buttons TASK + COMMANDS RUN
def createRest(topMenu):
    rest = Tkinter.Button(topMenu, text ="Rest", command=runRest)
    rest.grid(column=0,row=0)

def runRest():    
    os.system('python ld_mslRest.py')
    
def createSleepiness(topMenu):
    sleepiness = Tkinter.Button(topMenu, text ="Sleepiness", command=runSleepiness)
    sleepiness.grid(column=0,row=1)

def runSleepiness():    
    os.system('python ld_mslSleepiness.py')    
    
def createVerification(topMenu):
    verification = Tkinter.Button(topMenu, text ="Verification", command=runVerification)
    verification.grid(column=0,row=2)
    
def runVerification():    
    os.system('python ld_mslVerification.py')    
    
def createIntro(topMenu):
    intro = Tkinter.Button(topMenu, text=' Intro ', command=runIntro)
    intro.grid(column=0,row=3)

def runIntro():
    os.system('python ld_mslIntro.py')        
    
def createTraining(topMenu):
    training = Tkinter.Button(topMenu, text ="Training", command=runTraining)
    training.grid(column=0,row=4)

def runTraining():
    os.system('python ld_mslTask.py')        
    
def chooseTask():
    task = Tkinter.Tk()
    task.title('MSL Tasks')
    task.grid()
    createRest(task)
    createVerification(task)    
    createIntro(task)    
    createTraining(task)    
    task.mainloop()
    
if __name__ == "__main__":
    chooseTask()
    
