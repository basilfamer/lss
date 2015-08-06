import curses
import os
import sys

search = ""
argId = 0

for arg in sys.argv:
	if argId > 0:
		search = arg
	argId+=1

scroll = 0
selected = 0

if search in ["help","-h","-help","-H","--h"]:
	print "lss: usage: lss [substring]"
	sys.exit()

scr = curses.initscr()
scr.border(10)

curses.curs_set(0)
curses.noecho()
scr.keypad(1)

def listDir(directory):
	ret = os.listdir(directory)
	dotrets = []
	ret2 = []
	for thing in ret:
		if search in thing:
			if thing.startswith("."):
				dotrets.append(thing)
			else:
				ret2.append(thing)
	for thing in dotrets:
		ret2.append(thing)
	return ret2

files = listDir(os.curdir)

def drawLines():
    for f in files[0+scroll:20+scroll]:
        if f == files[selected]: 
            scr.addstr(f + '\n', curses.A_STANDOUT)  
        elif os.path.isdir(f):
            scr.addstr(f + '\n', curses.A_BOLD)  
        else:    
            scr.addstr(f + '\n')

    scr.addstr("\nPress V to open in Vim\n")
    scr.addstr("Press Q to quit\n",curses.A_BOLD)


while(True):
    scr.clear()
    drawLines()
    event = scr.getch()
    if event==curses.KEY_UP: 
    	if selected > 0:
          selected -= 1
        else:
          selected = len(files)-1
          scroll = selected - 10
        if scroll > 0 and selected < 10+scroll:
          scroll -= 1
    if event==curses.KEY_DOWN:
    	if selected < len(files)-1:
        	selected += 1
       	else:
       		selected = 0
       		scroll = 0
        if selected > 10+scroll:
            scroll += 1
    if event==ord('v'):
      os.system('vim ' + files[selected])
    if event==ord('q'):
        break
    if event==curses.KEY_RIGHT:
    	search = ""
        if os.path.isdir(files[selected]):
			directory = files[selected]
			files = listDir(directory)
			os.chdir(directory)
			selected = 0
			scroll = 0
       	else:
       		os.system('open ' + files[selected])
       		break
    if event==curses.KEY_LEFT:
    	search = ""
        files = listDir('..')
        os.chdir('..')
        selected = 0
        scroll = 0

curses.endwin()
