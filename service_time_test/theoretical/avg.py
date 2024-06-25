import json

import sys

def avg_response_time(logName:str): #'response_times_B1_B2_D1.log'
    with open(logName, 'r') as f:
        
        api=[]
        db=[]
        
        for i,line in enumerate(f):
            #print(i,line)
            data = json.loads(line)
            
            api.append(data["apiServiceTime"])
            db.append(data["dbServiceTime"])
        
        ST_Api=(sum(api)/len(api)) / 1000
        ST_Db = ((sum(db)/len(db)) / 1000)
        
        #print("Before query: ", ST_Api1)
        #print("After query: ", ST_Api2)
        #print("Query: ", ST_Db)
        
        result = {"ST_Api":ST_Api, "ST_Db":ST_Db}
        
        #print(f"avg response time '{logName}':",result)
        
        return result

if __name__ == '__main__':
    
    args = sys.argv[1:]
    
    print(args)
    
    avg_response_time(args[0])