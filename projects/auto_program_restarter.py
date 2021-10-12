import argparse
import os
import time
import subprocess, sys

#python projects\auto_program_restarter.py -f projects\ai.py -c "ping www.google.com -t"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file_location", help="Program to start track.")
    parser.add_argument("-c", "--command", dest="command", help="Command to execute if file changed.")
    return parser.parse_args()

class Watcher(object):
    running = True

    def __init__(self, watch_file, cmd=None):
        self.filename = watch_file
        self.func = cmd

    def look(self):
        global p, c
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            if self.func is not None:
                if self.func is not default_action:
                    try:
                        subprocess.Popen("taskkill /F /T /pid {pid}".format(pid=c.pid), stdout=subprocess.PIPE, shell=True)
                    except NameError:
                        pass
                    print("\nFile Changed")
                    custom_action(self.func)
                else:
                    try:
                        subprocess.Popen("taskkill /F /T /pid {pid}".format(pid=c.pid), stdout=subprocess.PIPE, shell=True)
                    except NameError:
                        pass
                    print("\nFile Changed")
                    self.func()

    def watch(self):
        print('\nStarted\nFile:%s\n'%(self.filename))
        self._cached_stamp = os.stat(self.filename).st_mtime
        while self.running:
            try:               
                time.sleep(1)
                self.look() 
            except KeyboardInterrupt: 
                try:
                    subprocess.Popen("taskkill /F /T /pid {pid}".format(pid=c.pid),stdout=subprocess.PIPE , shell=True)
                except NameError:
                    pass
                print('\nDone')
                break 
            except FileNotFoundError:
                print('\nFile Not Found')
                break
            except AttributeError:
                pass
            except: 
                print("Unhandled Error %s" % sys.exc_info()[0])

def custom_action(cmd):
    global c
    c = subprocess.Popen('{}'.format(cmd), stdout=subprocess.PIPE, shell =True)

def default_action():
    global c
    c = subprocess.Popen('python "F:/vishal/codings/python files/PycharmProjects/Gui/projects/GUI_CALC.py"', stdout=subprocess.PIPE, shell=True)


options = get_arguments()
if options.file_location:
    watcher = Watcher(options.file_location, options.command)
    watcher.watch()  # start the watch going
elif options.command and not options.file_location:
    print("\nCant execute a command without a file.")
else:
    default_action()
    watcher = Watcher("F:\\vishal\\codings\\python files\\PycharmProjects\\Gui\\projects\\Gui_Calc_Functions.py", default_action)  # also call custom action function
    watcher.watch()  # start the watch going

