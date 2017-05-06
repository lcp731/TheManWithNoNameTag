import inspect
import time
import base
import hitboxes
import keys
import sprites
import rooms
import tools
import objects
import sound

__authors__ = ["LeapBeforeYouLook", "Ramaraunt"]

def log(*msgs):
	curframe = inspect.currentframe()
	calframe = inspect.getouterframes(curframe, 2)
	calname = calframe[1][3]
	string = "[STELLAR] (%s - %s) %s" % (calname, time.time(), ", ".join(msgs))
	print string