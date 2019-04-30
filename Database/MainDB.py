"""
A class defined to create and manage the database intended to contain simulation results
@author: Pooya Bagheri
"""

import os
import warnings
from sqlalchemy import create_engine


class Database: #object of this class handles creation and modifications to database recording simulation results
    def __init__(self,Input,Loads):
        FileName='SimResults'+Input['Systems'][Input['SysID']]+'Case'+str(Input['CaseStudyID']) #Name of DB file
        self.__FilePath=Input['dir_path']+'\\OutputDBs\\'+FileName+'.db' #Path of DB file
        try: #our DB engine cannot overwrite, so we delete the previous DB with the same SysID and CaseID  
            os.remove(self.__FilePath)
        except: 
            print('No need to remove DB')
        self.__engine = create_engine('sqlite:///'+self.__FilePath, echo=False)
        self.RunSQLfile(Input['dir_path']+'/Database/CreateTables.sql') #running SQL scripts to create tables
        self.__FeederNodesInfo=None #this will be assigned during the first appending of results
        # Creating a load dataframe by keeping LoadID column
        #this dataframe will be used to insert load information for each new instant into the database
        self.__LoadsInfo=Loads.filter(['LoadID'],axis=1) 
        #creating two extra empty columns that will be filled at each instant before insertaion into database
        self.__LoadsInfo['InstantID'],self.__LoadsInfo['Scale']=None,None
     
    def AppendResults(self,InstantInfo,LoadProfile,SimResults):
        #breaking down the input simulation result
        Vdata=SimResults['Vdata']
        PlossData=SimResults['PlossData']
        
        #Feeder Nodes are only required to be added once to database:
        if self.__FeederNodesInfo is None: 
            self.__FeederNodesInfo=Vdata[['NodeID','Bus','Phase']]
            self.AppendNodes()
        #Warning the user if the nodes change during simulation:
        elif max(self.__FeederNodesInfo['NodeID']!= Vdata['NodeID']):
            warnings.warn('Feeder Nodes (or their sequence) are changing during simulation!')
        
        # Adding to database the Time,LoadProfile,Voltages and Ploss associated with each instant
        self.AppendTime(InstantInfo)
        InstantID=InstantInfo['InstantID'] #extracting InstantID for the rest of data insertion
        self.AppendLoadProfile(InstantID,LoadProfile)
        self.AppendVoltages(InstantID,Vdata[['NodeID','Vmag','Vang']])
        self.AppendPloss(InstantID,PlossData)
        
    def AppendNodes(self):
        #Creating Nodes table in database based off its Pandas dataframe
        self.__FeederNodesInfo.to_sql('Nodes', con=self.__engine, if_exists='append',index=False)
    
    def AppendTime(self,Info):
        #Run SQL query to insert instant data into Database
        self.__engine.execute("""
        INSERT INTO Instants (InstantID,Day,Hour,Minute,Second)
        VALUES (%d,%d,%d,%d,%d);
        """ % (Info['InstantID'],Info['Day'],Info['Hour'],Info['Minute'],Info['Second']))
        
    def  AppendLoadProfile(self,InstantID,LoadProfile):
        #Updating panda dataframe including instant load profile information
        self.__LoadsInfo.loc[:,'Scale']=LoadProfile
        self.__LoadsInfo.loc[:,'InstantID']=InstantID
        #Appending the dataframe into the LoadProfiles table of database:
        self.__LoadsInfo.to_sql('LoadProfiles', con=self.__engine, if_exists='append',index=False)
        
    def AppendVoltages(self,InstantID,Vdata):
        Vdata.loc[:,'InstantID']=InstantID #adding instant ID column
        #Appending the voltage dataframe into Voltages table of database
        Vdata.to_sql('Voltages', con=self.__engine, if_exists='append',index=False)        
        
    def AppendPloss(self,InstantID,Ploss):
        #Run SQL query to insert Ploss data into Database
        self.__engine.execute("""
        INSERT INTO Losses (InstantID,Ploss)
        VALUES (%d,%f);
        """ % (InstantID,Ploss))
    
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
                    
    def GetDBfilePath(self):
        return self.__FilePath                    

                
        