import os
import warnings
from sqlalchemy import create_engine

class Database: #object of this class handles creation and modifications to database recording simulation results
    def __init__(self,Input,Loads):
        FileName='SimResults'+Input['Systems'][Input['SysID']]+'Case'+str(Input['CaseStudyID']) #Name of DB file
        FilePath=Input['dir_path']+'\\OutputDBs\\'+FileName+'.db'
        try: #our DB engine cannot overwrite, so we delete the previous DB with the same SysID and CaseID  
            os.remove(FilePath)
        except: 
            print('No need to remove DB')
        self.__engine = create_engine('sqlite:///'+FilePath, echo=False)
        self.RunSQLfile(Input['dir_path']+'/Database/CreateTables.sql') #running SQL scripts to create tables
        self.__FeederNodes=None
     
    def AppendResults(self,InstantInfo,LoadProfile,SimResults):
        Vdata=SimResults['Vdata']
        PlossData=SimResults['PlossData']
        InstantID=InstantInfo['InstantID']
        if not self.__FeederNodes:
            self.__FeederNodes=Vdata[['NodeID','Bus','Phase']]
        elif max(self.__FeederNodes['NodeID']!= Vdata['NodeID']):
            warnings.warn('Feeder Nodes (or their sequence) are changing during simulation!')
        self.AppendTime(InstantInfo)
        self.AppendLoadProfile(InstantID,LoadProfile)
        self.AppendVoltages(InstantID,Vdata[['NodeID','Vmag','Vang']])
        self.AppendPloss(InstantID,PlossData)
        
            
            
    
    def RunSQLfile(self,file):
        sql_file = open(file,'r') # Open the .sql file
        sql_command = '' # Create an empty command string
        for line in sql_file: # Iterate over all lines in the sql file
            if line[:2]!='--': # Ignore commented lines
                # Append line to the command string
                sql_command += line.strip('\n')
                # If the command string ends with ';', it is a full statement
                if sql_command[-1]==';':
                    # Execute the sql statement 
                    self.__engine.execute(sql_command)
                    sql_command = '' #make SQl statement empty for next one

                
        