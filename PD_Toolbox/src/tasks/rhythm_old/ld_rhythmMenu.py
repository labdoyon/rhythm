# ABore - 6 Avril 2017
# CRIUGM
# -*- coding: utf-8 -*-

from psychopy import gui  #fetch default gui handler (qt if available)
from ld_config import rhythm_freq, rhythm_nbBlocks, rhythm_shortRest, rhythm_durRest, rhythm_halfBlockDuration, fullScreen
import os
import Tkinter

def getParamMenu():
    # create a DlgFromDict
    info = {'Observer':['ABoutin', 'EGabitov'],
            
        'freq':rhythm_freq,
        'nbBlocks':rhythm_nbBlocks,
        'shortRest':rhythm_shortRest,
        'durRest':rhythm_durRest,
        'halfBlockDuration':rhythm_halfBlockDuration,
        'language':['French', 'English'],
        'fullScreen':fullScreen}
    
    infoDlg = gui.DlgFromDict(dictionary=info, title='Stim Experiment - v0.1',
        order=['Observer','freq','nbBlocks','shortRest','durRest','halfBlockDuration','language','fullScreen'])

    if infoDlg.OK:  # this will be True (user hit OK) or False (cancelled)
        info['language'] = checkLanguage(info['language'])
        return info

def checkLanguage(currLanguage):
    if currLanguage == 'French': 
        return 0
    elif currLanguage == 'English':
        return 1
    
    
if __name__ == "__main__":
    getParamMenu()
    
