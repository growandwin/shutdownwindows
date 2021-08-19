from appJar import gui
import os
import threading
import time
from pynput.keyboard import Key, Controller

#cancel shutdown decorator before starting new countdown, otherwise the new time wont work
def cancel(button):
    def wrapper(*args, **kwargs):
        command = 'shutdown -a'
        print(command)
        os.system(command)
        button(*args, **kwargs)
    return wrapper

@cancel
def cancelOnce(button):
    pass

@cancel
def shutdownNow(button):
    command = 'shutdown -s -t 1'
    print(command)
    os.system(command)

@cancel
def shutdown(seconds):
    command = 'shutdown -s -t ' + str(seconds)
    print(command)
    os.system(command)

def min(button):
    minutesTable = [int(s) for s in button.split() if s.isdigit()]
    minutesToShutdown = minutesTable[0]
    print(minutesToShutdown)
    shutdown(minutesToShutdown*60)
    minutesToPressEnter = minutesToShutdown - 10
    x = threading.Thread(target=pressEnterAfterDelay, args=(minutesToPressEnter,))
    x.start()

def pressEnterAfterDelay(minutes):
    if minutes >= 0:
        print("sleeping:" + str(minutes*60 + 3))
        time.sleep(minutes*60 + 3)
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    print("Enter pressed and released")


# GUI variable called app
app = gui("Shut down script by Jarek Growin", "400x200")
app.setBg("blue")
app.setFont(24)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("Shutdown", "Shutdown")
app.addButton("NOW", shutdownNow)
# just change the number of minutes to the ones you frequently use
app.addButton("20 min", min)
app.addButton("30 min", min)
app.addButton("45 min", min)
app.addButton("60 min", min)
app.addButton("90 min", min)
app.addButton("120 min", min)

# link the buttons to the function called press
app.addButtons(["Cancel"], cancelOnce)

# start the GUI
app.go()