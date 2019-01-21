# ABore - 6 Avril 2017
# CRIUGM
# -*- coding: utf-8 -*-

from psychopy import gui  #fetch default gui handler (qt if available)
from ld_config import congruency_durRest, output, stimuli, observers, subjectPrefix, fullScreen
import os
import Tkinter
from tkFileDialog import askopenfilename
from ld_utils import readDesign
import sys, time
import json

def getParamMenu(currTask):
	
	if currTask in 'Condition1':
		seqFile	= '6blocks_cond1_rccccr.txt'
	elif currTask in 'Condition2':
		seqFile	= '6blocks_cond2_rccccr.txt'

    # create a DlgFromDict
	info = {'Observer':observers,
			'durRest':congruency_durRest,
			'design': seqFile,
        	'language':['French', 'English'],
        	'subject':subjectPrefix,
        	'flipMonitor':False,
        	'fullScreen':fullScreen}
    
	infoDlg = gui.DlgFromDict(dictionary=info, title='Stim Experiment - v0.1',
        order=['Observer', 'subject', 'design', 'language', 'flipMonitor', 'fullScreen', 'durRest'],
        tip={'Observer': 'trained visual observer, initials', 'durRest': 'seconds'})

    
    #Tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    #filename = askopenfilename(initialdir=stimuli) # show an "Open" dialog box and return the path to the selected file
    #info['design'] = filename
    
	if infoDlg.OK:  # this will be True (user hit OK) or False (cancelled)
		info['language'] = checkLanguage(info['language'])
		json.dump(info, open(os.path.join(output,'congruency',info['subject']+'_'+currTask+'_'+time.strftime("%Y%m%d-%H%M%S")+'.cfg'),'a+'))
		info['design'] = readDesign(filename)
		return info
	else:
		sys.exit("Cancel Congruency")

def checkLanguage(currLanguage):
    if currLanguage == 'French': 
        return 0
    elif currLanguage == 'English':
        return 1
	
# Buttons TASK + COMMANDS RUN
def	createCond1(topMenu):
	rest =	Tkinter.Button(topMenu,	text ="Condition1", command=runCond1)
	rest.grid(column=0,row=0)

def	runCond1():	 
	os.system('python ld_congruencyTask.py Condition1')
	
def	createCond2(topMenu):
	sleepiness	= Tkinter.Button(topMenu, text ="Condition 2", command=runCond2)
	sleepiness.grid(column=0,row=1)

def	runCond2():	   
	os.system('python ld_congruencyTask.py Condition2')	  
	
def	chooseTask():
	task =	Tkinter.Tk()
	task.title('Arrow Tasks')
	task.grid()
	createCond1(task)
	createCond2(task)
	task.mainloop()
	
if __name__	== "__main__":
	chooseTask()