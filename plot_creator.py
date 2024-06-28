import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.text import TextPath

import sympy as sp
from sympy.solvers import solve
from sympy import symbols

import json

from bs4 import BeautifulSoup

def trafficEqSolver():
    
    B1,B2,D1,D2,T1 = symbols('B1,B2,D1,D2,T1')

    eq1 = sp.Eq(B1,T1+0.1*D1)
    eq2 = sp.Eq(B2,0.8*D1)

    eq3 = sp.Eq(D1,B1)
    eq4 = sp.Eq(D2,B2)

    eq5 = sp.Eq(T1,D2+0.1*D1)

    eq6 = sp.Eq(T1,1) # T1 = 1 -> ref station

    relative_visit_ratios = solve([eq1,eq2,eq3,eq4,eq5,eq6],dict=True)

    print("relative visit ratio:", relative_visit_ratios[0])
    
    new={}
    
    new["B1"]=relative_visit_ratios[0][B1]
    new["B2"]=relative_visit_ratios[0][B2]
    new["D1"]=relative_visit_ratios[0][D1]
    new["D2"]=relative_visit_ratios[0][D2]
    #new["T1"]=relative_visit_ratios[0][T1]
    
    return new
    
def serviceDemands(service_times:dict, relative_visit_ratios:dict):
    
    service_demands={} # V_i * u_i
    
    
    service_demands["B1"]=relative_visit_ratios["B1"]*service_times["B1"]
    service_demands["D1"]=relative_visit_ratios["D1"]*service_times["D1"]
    
    service_demands["B2"]=relative_visit_ratios["B2"]*service_times["B2"]
    service_demands["D2"]=relative_visit_ratios["D2"]*service_times["D2"]
    
    #service_demands["T1"]=relative_visit_ratios[T1]*1000
    
    print("service demands:", service_demands)
    
    bottleneck=max(service_demands, key= lambda x: service_demands[x])
    
    print("bottleneck:", bottleneck)
    
    return service_demands, bottleneck

def NOpt(service_demands:dict, thinking_time:float, bottleneck:str):
    
    n_opt=(sum(service_demands.values())+thinking_time)/service_demands[bottleneck]
    
    print("n_opt:",n_opt)
    
    return n_opt

def lower_bound(service_demands:dict, max_n_users:int, thinking_time:float, bottleneck:str):
    #R>=max(D,N*D_{b}-Z)
    
    D=sum(service_demands.values())
    
    Db=service_demands[bottleneck]
    
    users=range(1,max_n_users,1)
    
    down=(D,[(n,(n*Db)-thinking_time) for n in users])
    
    print("lower bound:", f"R>=max({D}, N*{Db}-{thinking_time})")
    
    return down 
    
def upper_bound(service_demands:dict, max_n_users:int, thinking_time:float, bottleneck:str):
    #X<=min( N/D+Z, 1/D_{b} )
    
    D=sum(service_demands.values())
    
    Db=service_demands[bottleneck]
    
    users=range(1,max_n_users,1)
    
    up=(1/Db,[(n,n/(D+thinking_time)) for n in users])
    
    print("upper bound:", f"X<=min(N/({D}+{thinking_time}), 1/{Db})")
    
    return up

def load_test_reader():
    data_path = "load_test/"

    X = []
    R = []
    users = range(50, 550, 50)

    for n_users in users:
        with open(f"{data_path}results_{n_users}/statistics.json", "r") as f:
            results = json.load(f)
            
            X.append(results["Transaction Controller"]["throughput"])
            R.append(results["Transaction Controller"]["meanResTime"]/1000)

    #print(X)
    #print(R)
    
    return users, X, R

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

def bounds_getter_printer():
    service_times = service_times_reader(n_cores=8)
    
    relative_visit_ratios=trafficEqSolver()
    service_demands, bottleneck = serviceDemands(relative_visit_ratios, service_times)

    n_optimal = NOpt(service_demands, thinking_time=1, bottleneck=bottleneck)
    lb = lower_bound(service_demands, max_n_users=500, thinking_time=1, bottleneck=bottleneck)
    ub = upper_bound(service_demands, max_n_users=500, thinking_time=1, bottleneck=bottleneck)
    
    return lb, ub, n_optimal

def MVA_data_reader(jmva_file:str):
    
    users=[]
    X=[]
    R=[]
    
    with open(jmva_file) as f:
        Bs_data = BeautifulSoup(f.read(), "xml")
        
        iterations = Bs_data.find_all('solutions', {"algCount":"1"})
        
        for iteration in iterations:
            n_users=float(iteration.get("iterationValue"))
            
            throughput=float(iteration.find("stationresults",{'station':"T1"}).find("measure",{'measureType':"Throughput"}).get("meanValue"))
            
            rt=-1
            for station in iteration.findAll("stationresults"):
                
                rt_station = float(station.find("measure",{'measureType':"Residence time"}).get("meanValue"))
                rt = rt + rt_station
                
            #print(f"n_users: {n_users}, throughput: {throughput}, response time: {rt}")
            
            X.append(throughput)
            R.append(rt)
            users.append(n_users)
            
    return users, X, R

def plots(users, X, R, Throughput_title:str, ResponseTime_title:str):
    
    marker='*'
    
    lb, ub, n_optimal = bounds_getter_printer()
    
    fig, ax= plt.subplots(figsize=(8, 6))
    
    ax.plot(users, X, label="Throughput")
    ax.plot([x[0] for x in ub[1]], [min(ub[0],x[1]) for x in ub[1]],label="upper bound", linestyle='dotted', color='red')
    
    stem=ax.scatter(n_optimal, ub[0], label="optimal number of users", marker=marker)
    #stem[1].set_linestyles("dashed")
    #stem[2].set_linestyle("dashed")
    #stem[0].set_color("darkgray")
    #stem[1].set_color("darkgray")
    #stem[2].set_color("darkgray")
    
    ax.legend()
    ax.grid()
    ax.set_title(Throughput_title)
    
    fig, ax= plt.subplots(figsize=(8, 6))
    
    ax.plot(users, R, label="Expected Response Time")
    ax.plot([x[0] for x in lb[1]], [max(lb[0], x[1]) for x in lb[1]],label="lower bound", linestyle='dotted', color='red')
    
    stem=ax.scatter(n_optimal, lb[0], label="optimal number of users", marker=marker)
    #stem[1].set_linestyles("dashed")
    #stem[2].set_linestyle("dashed")
    #stem[0].set_color("darkgray")
    #stem[1].set_color("darkgray")
    #stem[2].set_color("darkgray")
    
    ax.legend()
    ax.grid()
    ax.set_title(ResponseTime_title)
    
    plt.show()

def load_test_plots_with_theoretical_bounds():
    
    users, X, R = load_test_reader()
    
    plots(users, X, R, "Empirical throughput vs Number of users \n with theoretical bounds", "Empirical expected response time vs Number of users \n with theoretical bounds")

def MVA_plots_with_theoretical_bounds():

    users, X, R = MVA_data_reader("theoretical/MVA.jmva")
    
    plots(users, X, R, "Theoretical throughput (MVA) vs Number of users \n with theoretical bounds", "Theoretical expected response time (MVA) vs Number of users \n with theoretical bounds")

if __name__ == "__main__":
    MVA_plots_with_theoretical_bounds()
    #load_test_plots_with_theoretical_bounds()

