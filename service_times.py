import json

def avg_response_time(logName:str): #'response_times_B1_B2_D1.log'
    
    script_path="service_time_test/"
    
    with open(script_path+logName, 'r') as f:
        
        api=[]
        db=[]
        
        for i,line in enumerate(f):
            #print(i,line)
            data = json.loads(line)
            
            api.append(data["apiServiceTime"])
            db.append(data["dbServiceTime"])
        
        ST_Api=(sum(api)/len(api)) / 1000
        ST_Db = (sum(db)/len(db)) / 1000
        
        #print("Before query: ", ST_Api1)
        #print("After query: ", ST_Api2)
        #print("Query: ", ST_Db)
        
        result = {"ST_Api":ST_Api, "ST_Db":ST_Db}
        
        #print(f"avg response time '{logName}':",result)
        
        return result

def service_times_reader(n_cores:int):
    
    service_times={} 
    
    response_times_B1_D1=avg_response_time("ST_B1_D1.log") #search
    
    response_times_B2_D2=avg_response_time("ST_B2_D2.log") #click
    
    service_times["B1"]=response_times_B1_D1["ST_Api"]
    service_times["D1"]=response_times_B1_D1["ST_Db"]/(n_cores)
    
    service_times["B2"]=response_times_B2_D2["ST_Api"]
    service_times["D2"]=response_times_B2_D2["ST_Db"]/(n_cores)
    
    print("service times:", service_times)
    
    return service_times

if __name__ == '__main__':
    service_times_reader(8)