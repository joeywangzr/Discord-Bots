from datetime import datetime

def checkTime():
    if int(datetime.now().strftime("%H")) >= 7 and int(datetime.now().strftime("%H")) <= 11 and int(datetime.now().strftime("%M")) == 9:
        print("Drink Water!")
    else:
        pass
