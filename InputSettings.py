"""
This file contains/generates the input setting data required for the simulation
@author: Pooya Bagheri
"""

import os
from datetime import datetime

Input={
       'SysID': 1, #the ID of test system that is simulated. List of IDs- 1:
       'Systems':{1:'IEEE123Nodes'}, #ID of available test systems
       'CaseStudyID':1, #Assign a unique ID to each case study on a system 
       'TestStartTime': datetime(2010,1,1,0,0,0), #the abstract time of starting instant for the simulation on the test feeder
       'TestLength': 3*24*60, #in minutes
       'Resolution':60, # time resolution of simulation, in seconds
       'dir_path': os.path.dirname(os.path.realpath(__file__)), #active directory where the program is run from
       }