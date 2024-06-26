import sympy as sp
from sympy.solvers import solve
from sympy import symbols

from avg import avg_response_time

import numpy as np

import matplotlib.pyplot as plt

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
    new["T1"]=relative_visit_ratios[0][T1]
    
    return new


def service_times(n_cores:int):
    
    service_times={} 
    
    response_times_B1_D1=avg_response_time("ST_B1_D1.log") #search
    
    response_times_B2_D2=avg_response_time("ST_B2_D2.log") #click
    
    service_times["B1"]=response_times_B1_D1["ST_Api"]
    service_times["D1"]=response_times_B1_D1["ST_Db"]/(n_cores-1)
    
    service_times["B2"]=response_times_B2_D2["ST_Api"]
    service_times["D2"]=response_times_B2_D2["ST_Db"]/(n_cores-1)
    
    print("service times:", service_times)
    
    return service_times
    
def serviceDemands(service_times:dict, relative_visit_ratios:dict):
    
    service_demands={} # V_i * u_i
    
    
    service_demands["B1"]=relative_visit_ratios["B1"]*service_times["B1"]
    service_demands["D1"]=relative_visit_ratios["D1"]*service_times["D1"]
    
    service_demands["B2"]=relative_visit_ratios["B2"]*service_times["B2"]
    service_demands["D2"]=relative_visit_ratios["D2"]*service_times["D2"]
    
    #service_demands["T1"]=relative_visit_ratios[T1]*1000
    
    bottleneck=max(service_demands, key= lambda x: service_demands[x])
    
    print("service demands:", service_demands)
    
    print("bottleneck:", bottleneck)
    
    return service_demands, bottleneck

def total_throughput():
    pass

def utilizations(service_demands:dict, n_users:int):
    
    utilizations={}
    X1=1*n_users
    
    utilizations["B1"]=service_demands["B1"]*X1
    utilizations["D1"]=service_demands["D1"]*X1
    
    utilizations["B2"]=service_demands["B2"]*X1
    utilizations["D2"]=service_demands["D2"]*X1
    
    #utilizations["T1"]=service_demands["T1"]*X1
    
    print("utilizations:", utilizations)
    
    return utilizations

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
    
    #print(down)
    
    return down 
    
def upper_bound(service_demands:dict, max_n_users:int, thinking_time:float, bottleneck:str):
    #X<=min( N/D+Z, 1/D_{b} )
    
    D=sum(service_demands.values())
    
    Db=service_demands[bottleneck]
    
    users=range(1,max_n_users,1)
    
    up=(1/Db,[(n,n/(D+thinking_time)) for n in users])
    
    #print(up)
    
    return up

def plot_boundaries():
    
    fig, axs = plt.subplots(
        nrows=2, ncols=1,
        figsize=(5, 10)
    )
    
    down=lower_bound(service_demands, max_n_users=500, thinking_time=1, bottleneck=bottleneck)
    
    up=upper_bound(service_demands, max_n_users=1000, thinking_time=1, bottleneck=bottleneck)
    
    axs[0].plot([x[0] for x in up[1]], [min(up[0],x[1]) for x in up[1]],label="upper bound")
    axs[0].set_title("Upper Bound")
    
    axs[1].plot([x[0] for x in down[1]], [max(down[0], x[1]) for x in down[1]],label="lower bound")
    axs[1].set_ylim(0,0.3)
    axs[1].set_title("Lower Bound")
    
    plt.show()

if __name__ == "__main__":
    
    relative_visit_ratios=trafficEqSolver()
    
    service_times=service_times(n_cores=8)
    
    service_demands, bottleneck=serviceDemands(relative_visit_ratios, service_times)
    
    n_optimal = NOpt(service_demands, thinking_time=1, bottleneck=bottleneck)
    
    #lower_bound(service_demands, max_n_users=500, thinking_time=1, bottleneck=bottleneck)
    
    #upper_bound(service_demands, max_n_users=1000, thinking_time=1, bottleneck=bottleneck)
    
    #utilizations=utilizations(service_demands, n_users=100)
    
    plot_boundaries()
