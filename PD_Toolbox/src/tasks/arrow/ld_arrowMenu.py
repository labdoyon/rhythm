# ABore	- 6	Avril 2017
# CRIUGM
# -*- coding: utf-8	-*-

from psychopy import gui  #fetch default gui handler (qt if	available)
from ld_config import arrow_seqA, arrow_seqB, arrow_nbBlocks, arrow_nbKeys,	arrow_durRest, flipMonitor,	fullScreen,	observers, output, subjectPrefix
import os, sys, json, time
import Tkinter

def	getParamMenu(currTask):
	
	if	currTask in	'Run1':
		seqFile	= 'arrow_v1.txt'
	elif currTask in 'Run2':
		seqFile	= 'arrow_v2.txt'
	elif currTask in 'Run3':
		seqFile	= 'arrow_v3.txt'
	elif currTask in 'Run4':
		seqFile	= 'arrow_v4.txt'
	elif currTask in 'Run5':
		seqFile	= 'arrow_v5.txt'
	elif currTask in 'Run6':
		seqFile	= 'arrow_v6.txt'

	# create a	DlgFromDict
	info =	{'Observer':observers,
		'seqFilename':seqFile,
		'durRest':arrow_durRest,
		'language':['French',	'English'],
		'flipMonitor':flipMonitor,
		'fullScreen':fullScreen,
		'subject':subjectPrefix}
	
	infoDlg = gui.DlgFromDict(dictionary=info,	title='Stim	Experiment - v0.1',
		order=['Observer', 'subject', 'seqFilename', 'language', 'flipMonitor', 'fullScreen', 'durRest'],
		tip={'Observer': 'trained	visual observer, initials',	'durRest': 'seconds' , 'flipMonitor':'Doesnt work yet'})

	if	infoDlg.OK:	 # this	will be	True (user hit OK) or False	(cancelled)
		info['language'] = checkLanguage(info['language'])
		json.dump(info, open(os.path.join(output,'arrow',info['subject'] + '_'+currTask+'_'+time.strftime("%Y%m%d-%H%M%S")+'.cfg'),'a+'))
		return info
	else:
		sys.exit("Cancel ARROW")

def	checkLanguage(currLanguage):
	if	currLanguage ==	'French': 
		return 0
	elif currLanguage == 'English':
		return 1
	
# Buttons TASK + COMMANDS RUN
def	createV1(topMenu):
	rest =	Tkinter.Button(topMenu,	text ="Run 1", command=runV1)
	rest.grid(column=0,row=0)

def	runV1():	 
	os.system('python ld_arrowTask.py Run1')
	
def	createV2(topMenu):
	sleepiness	= Tkinter.Button(topMenu, text ="Run 2", command=runV2)
	sleepiness.grid(column=0,row=1)

def	runV2():	   
	os.system('python ld_arrowTask.py Run2')	  
	
def	createV3(topMenu):
	verification =	Tkinter.Button(topMenu,	text ="Run 3", command=runV3)
	verification.grid(column=0,row=2)
	
def	runV3():	 
	os.system('python ld_arrowTask.py Run3')

def	createV4(topMenu):
	verification =	Tkinter.Button(topMenu,	text ="Run 4", command=runV4)
	verification.grid(column=0,row=3)
	
def	runV4():	 
	os.system('python ld_arrowTask.py Run4')
	
def	createV5(topMenu):
	verification =	Tkinter.Button(topMenu,	text ="Run 5", command=runV5)
	verification.grid(column=0,row=4)
	
def	runV5():	 
	os.system('python ld_arrowTask.py Run5')
	
def	createV6(topMenu):
	verification =	Tkinter.Button(topMenu,	text ="Run 6", command=runV6)
	verification.grid(column=0,row=5	)
	
def	runV6():	 
	os.system('python ld_arrowTask.py Run6')	
	
	
def	chooseTask():
	task =	Tkinter.Tk()
	task.title('Arrow Tasks')
	task.grid()
	createV1(task)
	createV2(task)
	createV3(task)
	createV4(task)
	createV5(task)
	createV6(task)	
	task.mainloop()
	
if __name__	== "__main__":
	chooseTask()