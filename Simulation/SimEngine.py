"""
Simulation engine that employs OpenDSS API
"""
import win32com.client
from pandas import DataFrame as df
import pandas as pd

class SimEngine:
    DSSfilePaths={'IEEE123Nodes':r"\Simulation\IEEE123Bus\IEEE123Master.dss"}
    def __init__(self,SysName,dir_path): 
        #Initialize OpenDSS API as an object inside this class:
        try:
            self.DSSObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
        except:
            print("Unable to start the OpenDSS Engine")
            raise SystemExit
        self.DSS=self.DSSObj.Text #Creating shortcut for entering/reading OpenDSS command/result
        self.DSSCircuit=self.DSSObj.ActiveCircuit #Creating a shortcut to access active circuit object in OpenDSS
        self.DSS.command = "Compile '"+dir_path+self.DSSfilePaths[SysName]+"'"    
    
    def GetBaseLoads(self): #extracting base load information from system model
        repeat=1
        Loads=[]
        LoadItems=self.DSSCircuit.Loads
        LoadItems.First
        while repeat: #this loop iteratively reads load information from OpenDSS object and save into 'Loads' list
            Loads.append([LoadItems.name,LoadItems.kW,LoadItems.kvar])
            repeat=LoadItems.Next
        Loads=df(Loads,columns=["Name","kW","kvar"]) #creating Pandas dataframe containing loads information
        Loads.loc[:,'LoadID']=Loads.index+1
        Loads=Loads[["LoadID","Name","kW","kvar"]] #rearranging dataframe column sequence
        return Loads
    
    def UpdateLoad(self,load,scale):
        self.DSS.command="load.%s.kw=%f" % (load['Name'],load['kW']*scale)
        self.DSS.command="load.%s.kvar=%f" % (load['Name'],load['kvar']*scale)
        
    def SolveCircuit(self):    
        self.DSS.command="solve"
        
    def ReadVoltages(self):
        self.DSS.command="Export Voltages"
        V=pd.read_csv(self.DSS.result,usecols=[0,2,4,5,6,8,9,10,12,13])
        Parts=[None]*3
        for i in range(3):
            n=str(i+1)
            Parts[i]=V.filter(['Bus',' Node'+n,' pu'+n,' Angle'+n],axis=1)
            Parts[i].columns=['Bus','Phase','Vmag','Vang']
        combined=pd.concat(Parts)
        combined=combined[combined.Phase!=0]
        combined=combined.reset_index(drop=True)
        combined.loc[:,'NodeID']=combined.index + 1
        return combined
    
    def ReadPloss(self):
        self.DSS.command="Export Losses"
        Losses=pd.read_csv(self.DSS.result,usecols=[1])
        return float(Losses.sum(axis=0))/10**3
        
        