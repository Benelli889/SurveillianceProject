#!/usr/bin/python
import os, time, sys
from datetime import datetime
from datetime import timedelta
from TimerClass import TimerClass
from LoggerClass import LoggerClass


class SurveillanceFilesClass:
    #PathSurveillianceStation = '/home/pi/Projects/Surveillance/@Snapshot/@PushServ/'
    PathSurveillianceStation = '/volume1/surveillance/@Snapshot/@PushServ/'

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
Log.Configure('/volume1/homes/ArndtDev', 'Surveillance')


while True:
    try:
        SurveillanceFiles.ReadSurveillanceFiles()

        if SurveillanceFiles.NewFileAvailable():
            Log.MsgFrequency("NewFileAvailable")

            if Timer.State() == Timer.STOPPED:
                Timer.Start()
                print (" Timer started")
                Log.Msg("Timer started: " + "{}".format(Timer.State()))
                time.sleep(3)
                os.system("curl -s http://192.168.178.49/cm?cmnd=power1%201")
                os.system("curl -s http://192.168.178.55/cm?cmnd=power1%201")
    
    except:
        print ("Interrupt error")
        sys.exit()

    if Timer.State() == Timer.STARTED:
        if Timer.TimerRunUp():
            print (" Timer run up")
            Log.Msg("Timer started: " + "{}".format(Timer.State()))
            #GPIO.output( pinList[1], GPIO.LOW)
            os.system("curl -s http://192.168.178.49/cm?cmnd=power1%200")
            os.system("curl -s http://192.168.178.55/cm?cmnd=power1%200")

    print '------------------'
    print SurveillanceFiles.NumberFilesStrored
    print '{:%H:%M:%S}'.format(datetime.now()) 
    print 'Timer.State()', Timer.State()
    print '------------------'
    Log.MsgFrequency("NumberFilesStrored: {}".format(SurveillanceFiles.NumberFilesStrored))
    
    SurveillanceFiles.StoreLastCycleK1()

    # Wait
    time.sleep(2)
    
