"""

@author: Pooya
"""

#Importing Project packages:
from InputSettings  import Input
from Simulation.MainSim import Simulations
from Simulation.LoadProfGen import LoadProfileGen
from Database.MainDB import Database




Simulation=Simulations(Input) #initialize simulation object
LoadProfGen=LoadProfileGen(Input,Simulation.GetBaseLoads())
DB=Database(Input,Simulation.GetBaseLoads())

temp=[]
while LoadProfGen.ContinueSimulation():
    LoadProfile=LoadProfGen.NextLoadProfile()
    Simulation.ModifyLoads(LoadProfile)
    #DB.AppendResults(LoadProfGen.GetTimeInstantInfo(),LoadProfile,Simulation.GetResults())
    LoadProfGen.ReportProgress()
'''
for i,conductor in enumerate(Cases.conductors):
   Sim.BreakConductor(conductor)
   for j,LoadProf in enumerate(Cases.LoadProfiles):
        Sim.ModifyLoads(LoadProf)
        DB.save_result(Sim.get_result())
        print('%.1f%% Done, Time passed: %s' % (Cases.CompltedPerc(i,j),Sim.GetElapsedTime()))
   Sim.ResetConductors()    
print(DB) #gives the information on created DB from simulation results   
   '''