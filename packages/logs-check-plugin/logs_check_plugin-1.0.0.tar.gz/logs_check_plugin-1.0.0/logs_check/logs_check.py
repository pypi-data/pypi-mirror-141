#
# documentation:
import requests
import json

# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

class Logs:
    def __init__(self, filelocation):
        
        #initial
        self.filelocation = filelocation
    
    def check_logs(self, outdated_minutes):

        #variables
        retrcode = OK

        count = 0

        for line in (open(outdated_minutes)).readlines():

            if 'deadlock' not in line:
                pass
            else:
                print(f"Deadlock:")
                print(line.strip())
                retrcode = CRITICAL
                count += 1
        

        return retrcode, count
