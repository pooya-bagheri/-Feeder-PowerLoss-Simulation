"""
Simulation Model Class
@author: Pooya Bagheri
"""

from Simulation.SimEngine import SimEngine

class Simulations: #Takes care of simulations using OpenDSS API
    def __init__(self,Input):
        self.__SysName=Input['Systems'][Input['SysID']]
        self.__Engine=SimEngine(self.__SysName,Input['dir_path']) #initialize simulation engine
        self.__BaseLoads=self.__Engine.GetBaseLoads()
    
    def ModifyLoads(self,Profile):
        for i,load in self.__BaseLoads.iterrows():
            self.__Engine.UpdateLoad(load,Profile[i])
    
    def GetBaseLoads(self):
        return self.__BaseLoads
    
    def GetSysName(self):
        return self.__SysName
    
    def GetResults(self):
        self.__Engine.SolveCircuit()
        Vdata=self.__Engine.ReadVoltages()
        PlossData=self.__Engine.ReadPloss()
        return {'Vdata':Vdata,'PlossData':PlossData}
        
  