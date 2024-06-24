import json

import sys

def avg_response_time(logName:str): #'response_times_B1_B2_D1.log'
    with open(logName, 'r') as f:
        
        api1=[]
        api2=[]
        db=[]
        
        for line in f:
            data = json.loads(line)
            
            api1.append(data["apiServiceTime"])
            db.append(data["dbServiceTime"])
            api2.append(data["apiExtraServiceTime"])
            
        print("Before query: ", sum(api1)/len(api1))
        print("After query: ", sum(api2)/len(api2))
        print("Query: ", sum(db)/len(db))

if __name__ == '__main__':
    
    args = sys.argv[1:]
    
    avg_response_time(args[0])