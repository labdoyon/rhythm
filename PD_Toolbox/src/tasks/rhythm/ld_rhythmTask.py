from __future__ import division
import sys
import numpy as np
from expyriment import control, stimuli, io, design, misc
from expyriment.misc import constants
from expyriment.misc._timer import get_time
from ld_rhythmMenu import getParamMenu
from ld_messages import readyMessage

# Paramaters: generic
from ld_config import fullScreen, windowSize, restBGColor, textSize, goldColor, rhythm_execDuration, rhythm_execLongDuration, rhythm_execShortDuration, rhythm_imagineDuration

# Parameters: cross
from ld_config import regularCrossColor, restCrossColor, restCrossSize, restCrossThickness, blueCrossColor

# Parameters: lines
from ld_config import startPointLines, endPointLines, activeLineColour, deactiveLineColour, lineThickness

# Get name of the task
task = sys.argv[1]

#Menu
infos = getParamMenu(task)

if infos['fullScreen']:	# Check WindowMode and Resolution
	#control.defaults.window_mode = fullScreen
	#control.defaults.window_size = misc.get_monitor_resolution()
	print 'FullScreen: ON'
else:
	control.defaults.window_mode = fullScreen
	control.defaults.window_size = windowSize

exp = design.Experiment(task)  # Save experiment name: task
exp.add_experiment_info(['Subject: '])  # Save Subject Code
exp.add_experiment_info([infos['subject']])  # Save Subject Code

# Start Keyboard acquisition
trigger = io.Keyboard()
control.initialize(exp)

# Blanck Screen
bs = stimuli.BlankScreen(restBGColor)
bs.present(True, True)

# Crosses
greenFixCross = stimuli.FixCross(colour=regularCrossColor, size=restCrossSize, line_width=restCrossThickness)
greenFixCross.preload()
redFixCross = stimuli.FixCross(colour=restCrossColor, size=restCrossSize, line_width=restCrossThickness)
redFixCross.preload()
blackFixCross = stimuli.FixCross(colour=restBGColor, size=restCrossSize, line_width=restCrossThickness)
blackFixCross.preload()
#blueFixCross = stimuli.FixCross(colour=blueCrossColor, size=restCrossSize, line_width=restCrossThickness)
#blueFixCross.preload()

# WaitBars
activateLine1 = stimuli.Line(start_point= startPointLines[0], end_point=endPointLines[0] , line_width= lineThickness, colour=activeLineColour, anti_aliasing=10)
activateLine1.preload()
activateLine2 = stimuli.Line(start_point= startPointLines[1], end_point=endPointLines[1] , line_width= lineThickness, colour=activeLineColour, anti_aliasing=10)
activateLine2.preload()
activateLine3 = stimuli.Line(start_point= startPointLines[2], end_point=endPointLines[2] , line_width= lineThickness, colour=activeLineColour, anti_aliasing=10)
activateLine3.preload()

deactivateLines = [stimuli.Line(start_point= startPointLines[0], end_point=endPointLines[0] , line_width= lineThickness, colour=deactiveLineColour, anti_aliasing=10),
				   stimuli.Line(start_point= startPointLines[1], end_point=endPointLines[1] , line_width= lineThickness, colour=deactiveLineColour, anti_aliasing=10),	
				   stimuli.Line(start_point= startPointLines[2], end_point=endPointLines[2] , line_width= lineThickness, colour=deactiveLineColour, anti_aliasing=10)]

deactivateLines[0].preload()
deactivateLines[1].preload()
deactivateLines[2].preload()

#Text
instructions = stimuli.TextLine(  readyMessage[infos['language']],
								  position=(0, -.7),
								  text_font=None, text_size=textSize, text_bold=None, text_italic=None,
								  text_underline=None, text_colour=goldColor,
								  background_colour=restBGColor,
								  max_width=None)

# Tone used
tone1 = stimuli.Tone(50, 675)
tone1.preload()

# Init var
nBlock = 0
times = []
def readKeyboard():
	global exp
	global times
	key = exp.keyboard.check([49, 50, 51, 52, 121])
	if key is not None:
		times.append(exp.clock.time)

control.start(exp, auto_create_subject_id=True, skip_ready_screen=True)

nbBlock = 1

instructions.plot(bs)
bs.present(True, True)

trigger.wait(keys=[53], wait_for_keyup=True)

#activateLine1.plot(redFixCross.decompress())

bs.clear_surface()

redFixCross.plot(bs)
activateLine1.plot(bs)
activateLine2.plot(bs)
activateLine3.plot(bs)
bs.present(clear=True,update=True)

exp.clock.wait(infos['durRest'])

control.register_wait_callback_function(readKeyboard,exp)

while nbBlock <= infos['nbBlocks']:
	resetLine = 0
	greenFixCross.plot(bs)
	bs.present(False, True)
	startSync = get_time()

	nbip = 0
	for nbip in range(int(infos['syncDuration']*infos['freq'])):
		tone1.play()
		#tone1.play(maxtime=50)		
		exp.clock.wait(infos['beepEach']*1000)
		
		if nbip>infos['syncDuration']*infos['freq']-4:
			if resetLine<3:
				greenFixCross.plot(bs)
				deactivateLines[resetLine].plot(bs)
				bs.present(clear=False,update=True)
				resetLine +=1


	#	Reset lines
	if 'Sync' in task:
		greenFixCross.plot(bs)
	#else:
	#	blueFixCross.plot(bs)
		
	activateLine1.plot(bs)
	activateLine2.plot(bs)
	activateLine3.plot(bs)
	bs.present(False, True)

	if 'Sync' in task:
		exp.clock.wait(infos['execDuration']*1000)
	#else:
	#	exp.clock.wait(rhythm_imagineDuration*1000)
	#	greenFixCross.plot(bs)
	#	bs.present(False, True)
	#	exp.clock.wait(rhythm_execShortDuration*1000)
	
	bs.clear_surface()
	redFixCross.plot(bs)
	activateLine1.plot(bs)
	activateLine2.plot(bs)
	activateLine3.plot(bs)
	bs.present(True, True)
	exp.clock.wait(infos['durRest'])
	nbBlock += 1

control.end()
#control.unregister_wait_callback_function(readKeyboard)