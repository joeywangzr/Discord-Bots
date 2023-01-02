from datetime import datetime
timers = []
def initTimer(minutes): #minutes = minutes from now
    newMinutes = int(minutes)
    global timers
    currentTimeHour = int(datetime.now().strftime("%H")) #24 hour time
    currentTimeMinute = int(datetime.now().strftime("%M"))
    hours = newMinutes // 60
    newMinutes -= hours * 60
    targetTimeMinute = currentTimeMinute + newMinutes
    if targetTimeMinute >= 60:
        targetTimeMinute -= 60
        hours += 1
    targetTimeHour = currentTimeHour + hours
    if targetTimeHour >= 24:
        targetTimeHour -= 24
    targetTime = [targetTimeHour, targetTimeMinute]
    return(targetTime)

def checkTime():
    global timers
    for i in range(len(timers)):
        if timers[i][0] == datetime.now().strftime("%H") and timers[i][1] == datetime.now().strftime("%M"):
            print("Alarm!")
            timers.pop(i)
        else:
            pass

