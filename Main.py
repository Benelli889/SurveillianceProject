#!/usr/bin/python
import os, time, sys
from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO
from TimerClass import TimerClass
from LoggerClass import LoggerClass

GPIO.setmode(GPIO.BCM)
# Pin list for Relai-Board
pinList = [19, 26, 20,  21]
GPIO.setup(pinList[1], GPIO.OUT) 
GPIO.output(pinList[1], GPIO.LOW)
GPIO.setup(pinList[2], GPIO.OUT) 
GPIO.output(pinList[2], GPIO.LOW)


class SurveillanceFilesClass:
    #PathSurveillianceStation = "D:\\Daten\\03_Hobby\\Computer\\Raspberry\\Python"
    PathSurveillianceStation = '/home/pi/Projects/Surveillance/@Snapshot/@PushServ/'

    NumberFilesStrored = 0
    StoreLastElement = 0 
    fileDateArray = []

    def __INIT__(self):
        self.fileDateArray = []

    def ReadSurveillanceFiles(self):
        
        for filename in os.listdir(self.PathSurveillianceStation):
            self.fileDateArray.append(os.path.getmtime(self.PathSurveillianceStation + filename))

        # Sort list
        self.fileDateArray.sort()

        # Print List Elements
        for Filenames in self.fileDateArray:
            DateTimeObj = datetime.fromtimestamp(Filenames)
            #print '{:%Y-%m-%d %H:%M:%S}'.format(DateTimeObj)    

        self.NumberFilesStrored = len(self.fileDateArray)

    def NewFileAvailable(self): 
        #if len(fileDateArray) > NumberFilesStrored:
        if (self.StoreLastElement != 0) and (self.fileDateArray[-1] > self.StoreLastElement):
            return True

    def StoreLastCycleK1(self):
        self.StoreLastElement = self.fileDateArray[-1]
        self.fileDateArray = []


SurveillanceFiles = SurveillanceFilesClass()
Timer = TimerClass ()
#Timer Relais
Timer.SetTimerDuration(timedelta(weeks=0, days=0, seconds=20, microseconds=0, milliseconds=0, minutes=0, hours=0))
#Logger Text
Log = LoggerClass()
Log.Configure('/home/pi/Projects/SurveillianceProject', 'Surveillance')


while True:
    try:
        SurveillanceFiles.ReadSurveillanceFiles()

        if SurveillanceFiles.NewFileAvailable():
            Log.MsgFrequency("NewFileAvailable")

            if Timer.State() == Timer.STOPPED:
                Timer.Start()
                print (" Timer started")
                Log.Msg("Timer started: " + "{}".format(Timer.State()))
                GPIO.output( pinList[1], GPIO.HIGH)
                GPIO.output( pinList[2], GPIO.HIGH)
                time.sleep(3)
                GPIO.output( pinList[2], GPIO.LOW)
    
    except:
        print ("Interrupt error")
        GPIO.cleanup()
        sys.exit()

    if Timer.State() == Timer.STARTED:
        if Timer.TimerRunUp():
            print (" Timer run up")
            Log.Msg("Timer started: " + "{}".format(Timer.State()))
            GPIO.output( pinList[1], GPIO.LOW)

    print '------------------'
    print SurveillanceFiles.NumberFilesStrored
    print '{:%H:%M:%S}'.format(datetime.now()) 
    print 'Timer.State()', Timer.State()
    print '------------------'
    Log.MsgFrequency("NumberFilesStrored: {}".format(SurveillanceFiles.NumberFilesStrored))
    
    SurveillanceFiles.StoreLastCycleK1()

    # Wait
    time.sleep(2)

     
#Reset GPIO settings
GPIO.cleanup()
    
