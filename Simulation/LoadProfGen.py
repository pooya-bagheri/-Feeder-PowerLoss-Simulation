"""
Class defined to generate random load profiles for the simulation study
@author: Pooya Bagheri
"""

import random
import math
from datetime import timedelta, datetime

#an object of this class will be responsible to generate load profiles for different instants of simulation
class LoadProfileGen: 
    def __init__(self, Input, BaseLoads):
        self.__Nloads=len(BaseLoads.index) #extracting number of loads from the dataframe
        self.__InstantId=0
        self.__StartSimTime=Input['TestStartTime']
        self.__EndSimTime=Input['TestStartTime']+timedelta(minutes=Input['TestLength'])
        self.__ResolutionSimTime=timedelta(seconds=Input['Resolution'])
        self.ObjInitTime=datetime.now()
        self.__Coeffs=[None]
        self.__LastDay=None #this is used to generate new coeffs once entering a new day in simulation time
        
   
    def GetCurrentSimTime(self):
        return self.__StartSimTime+self.__InstantId*self.__ResolutionSimTime
    
    def ContinueSimulation(self):
        if self.GetCurrentSimTime() >= self.__EndSimTime:
            return False
        else:
            return True
    
    def __GenLoadProfCoeffs(self):
        self.__Coeffs=[{'f':round(random.triangular(0, 12, 2)),'Mag':random.uniform(0,.5),'phase':random.uniform(0,math.pi),'PeakTime':random.uniform(.2,0.8),'Peak':random.uniform(.5,1.5)} for _ in range(self.__Nloads)]
        
    def GetLoadProfCoeffs(self):
        return self.__Coeffs
        
    def GetTimeInstantInfo(self):
        t=self.GetCurrentSimTime()
        output=dict()
        output['Day']=t.date().day
        Time=t.time()
        output['Hour']=Time.hour
        output['Minute']=Time.minute
        output['Second']=Time.second
        output['InstantID']=self.__InstantId
        return output
        
    def ReportProgress(self):
        #printing the progress once per each 50 time instants
        if self.__InstantId % 50 == 0: 
            CompletedPortion=(self.GetCurrentSimTime()-self.__StartSimTime)/(self.__EndSimTime-self.__StartSimTime)*100
            print('%.1f%% is done, time passed:%s' % (CompletedPortion,str(datetime.now()-self.ObjInitTime)))
        
    def NextLoadProfile(self):
        self.__InstantId+=1 #Moving to next simulation time instant
        d=self.GetCurrentSimTime().date()
        if d!=self.__LastDay: #generate new coefficients if entering new day
            self.__GenLoadProfCoeffs()
            self.__LastDay=d
        t=self.GetCurrentSimTime().time()
        xt=(t.second+60*(t.minute+60*t.hour))/(24*60*60)
        Profile=[]
        for i in range(self.__Nloads):
            tp=self.__Coeffs[i]['PeakTime']
            yp=self.__Coeffs[i]['Peak']
            if xt<tp:
                LinearPart=xt/tp*(yp-0.5)+.5
            else:
                LinearPart=(xt-tp)/(1-tp)*(.5-yp)+yp
            Mag=self.__Coeffs[i]['Mag']
            f=self.__Coeffs[i]['f']
            phase=self.__Coeffs[i]['phase']
            SinusoidalPart=Mag*math.cos(2*math.pi*f*xt+phase)
            Profile.append(LinearPart+SinusoidalPart)
        return Profile
    





