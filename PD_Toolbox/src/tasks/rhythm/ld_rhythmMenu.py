# ABore - 6 Avril 2017
# CRIUGM
# -*- coding: utf-8 -*-

from __future__ import division
from psychopy import gui  #fetch default gui handler (qt if available)
from ld_config import congruency_durRest, output, stimuli, observers, subjectPrefix, fullScreen, rhythm_durRest, rhythm_nbBlocks, rhythm_execDuration, rhythm_syncDuration
import os
import Tkinter
from tkFileDialog import askopenfilename
from ld_utils import readDesign
import sys, time
import json

def getParamMenu(currTask):
    # create a DlgFromDict

	if 'L' in currTask:
		rhythm_freq = 0.5
	else:
		rhythm_freq = 1

	info = {'Observer':observers,
			'durRest':rhythm_durRest,
			'freq': rhythm_freq,
			'nbBlocks': rhythm_nbBlocks,
			'syncDuration': rhythm_syncDuration,
			'execDuration': rhythm_execDuration,
        	'language':['French', 'English'],
        	'subject':subjectPrefix,
        	'flipMonitor':False,
        	'fullScreen':fullScreen}
    
	infoDlg = gui.DlgFromDict(dictionary=info, title='Stim Experiment - v0.1',
        order=['Observer','subject', 'freq', 'nbBlocks', 'syncDuration', 'execDuration', 'language','flipMonitor','fullScreen','durRest'],
        tip={'Observer': 'trained visual observer, initials', 'durRest': 'ms'})

    
	if infoDlg.OK:  # this will be True (user hit OK) or False (cancelled)
		info['language'] = checkLanguage(info['language'])
		info['beepEach'] = 1/info['freq']
		json.dump(info, open(os.path.join(output,'rhythm',info['subject']+'_'+time.strftime("%Y%m%d-%H%M%S")+'.cfg'),'a+'))
		return info
	else:
		sys.exit("Cancel Rhythm")

def checkLanguage(currLanguage):
    if currLanguage == 'French': 
        return 0
    elif currLanguage == 'English':
        return 1
		
	# Buttons TASK + COMMANDS RUN
def	createCond1(topMenu):
	rest =	Tkinter.Button(topMenu,	text ="Sync long", command=runCond1)
	rest.grid(column=0,row=0)

def	runCond1():	 
	os.system('python ld_rhythmTask.py SyncL')
	
def	createCond2(topMenu):
	sleepiness	= Tkinter.Button(topMenu, text ="Sync short", command=runCond2)
	sleepiness.grid(column=0,row=2)

def	runCond2():	   
	os.system('python ld_rhythmTask.py SyncS')	  

def	chooseTask():
	task =	Tkinter.Tk()
	task.title('Rhythm Tasks')
	task.grid()
	createCond1(task)
	createCond2(task)
	task.mainloop()
	
if __name__	== "__main__":
	chooseTask()