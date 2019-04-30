"""
@author: Pooya Bagheri
"""

#Importing Project packages:
from InputSettings  import Input
from Simulation.MainSim import Simulations
from Simulation.LoadProfGen import LoadProfileGen
from Database.MainDB import Database




Simulation=Simulations(Input) #initialize simulation model (including OpenDSS API) according to the Input file
LoadProfGen=LoadProfileGen(Input,Simulation.GetBaseLoads()) #initialize the object to provide load profiles for the simulation study
DB=Database(Input,Simulation.GetBaseLoads()) #initialize database according to input file and list of loads in the test system

while LoadProfGen.ContinueSimulation(): #continue simulation until there is more load profile instants to be simulated
    #Obtain the next load profile
    LoadProfile=LoadProfGen.NextLoadProfile() 
    #Modify simulation model according to new load profile
    Simulation.ModifyLoads(LoadProfile)
    #Get new simulation result and insert it into the database
    DB.AppendResults(LoadProfGen.GetTimeInstantInfo(),LoadProfile,Simulation.GetResults())
    LoadProfGen.ReportProgress() #Display the simulation progress and the time elapsed

print(DB.GetDBfilePath()) #At the end, display the path to the generated output relational database containing simulation results!
