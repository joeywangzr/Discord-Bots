from datetime import datetime
alarmTime = [] #Hours they want the morning alarm 
def checkTime():
    global alarmTime
    if int(datetime.now().strftime("%H")) in alarmTime:
        print("Drink Water!")
    else:
        pass
