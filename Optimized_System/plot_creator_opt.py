import sympy as sp
from sympy.solvers import solve
from sympy import symbols

import ultraimport

import argparse

lower_bound = ultraimport('__dir__/../Current_System/plot_creator.py','lower_bound')
upper_bound= ultraimport('__dir__/../Current_System/plot_creator.py','upper_bound')
NOpt= ultraimport('__dir__/../Current_System/plot_creator.py','NOpt')

MVA_data_reader=ultraimport('__dir__/../Current_System/plot_creator.py','MVA_data_reader')

import matplotlib.pyplot as plt

def trafficEqSolverOpt1():
    
    B1,B2,DA1,DA2,DA2,DB1,DB2,T1 = symbols('B1,B2,DA1,DA2,DA2,DB1,DB2,T1')

    eq1 = sp.Eq(B1,T1+0.1*DA1+0.1*DB1)
    eq2 = sp.Eq(B2,0.8*DA1+0.8*DB1)

    eq3 = sp.Eq(DA1,0.5*B1)
    eq4 = sp.Eq(DA2,0.5*B2)
    
    eq5 = sp.Eq(DB1,0.5*B1)
    eq6 = sp.Eq(DB2,0.5*B2)

    eq7 = sp.Eq(T1,0.1*DA1+DA2+0.1*DB1+DB2)

    eq8 = sp.Eq(T1,1) # T1 = 1 -> ref station

    relative_visit_ratios = solve([eq1,eq2,eq3,eq4,eq5,eq6, eq7, eq8],dict=True)

    print("relative visit ratio:", relative_visit_ratios[0])
    
    new={}
    
    new["B1"]=relative_visit_ratios[0][B1]
    new["B2"]=relative_visit_ratios[0][B2]
    new["DA1"]=relative_visit_ratios[0][DA1]
    new["DA2"]=relative_visit_ratios[0][DA2]
    new["DB1"]=relative_visit_ratios[0][DB1]
    new["DB2"]=relative_visit_ratios[0][DB2]
    #new["T1"]=relative_visit_ratios[0][T1]
    
    return new

def trafficEqSolverOpt2():
    
    B1,B2,DA1,DA2,DA2,DB1,DB2,T1 = symbols('B1,B2,DA1,DA2,DA2,DB1,DB2,T1')

    eq1 = sp.Eq(B1,T1+0.1*DA1)
    eq2 = sp.Eq(B2,0.8*DA1)

    eq3 = sp.Eq(DA1,B1)
    eq4 = sp.Eq(DB2,B2)
    
    eq4 = sp.Eq(DA2,0)
    eq5 = sp.Eq(DB1,0)

    eq6 = sp.Eq(T1,DB2+0.1*DB1)

    eq7 = sp.Eq(T1,1) # T1 = 1 -> ref station

    relative_visit_ratios = solve([eq1,eq2,eq3,eq4,eq5,eq6,eq7],dict=True)

    print("relative visit ratio:", relative_visit_ratios[0])
    
    new={}
    
    new["B1"]=relative_visit_ratios[0][B1]
    new["B2"]=relative_visit_ratios[0][B2]
    new["DA1"]=relative_visit_ratios[0][DA1]
    new["DA2"]=relative_visit_ratios[0][DA2]
    new["DB1"]=relative_visit_ratios[0][DB1]
    new["DB2"]=relative_visit_ratios[0][DB2]
    #new["T1"]=relative_visit_ratios[0][T1]
    
    return new

def service_time():
    
    sts={'B1': 0.0016899999999999999, 'B2': 0.00171, 'DA1': 0.00257625, 'DB1': 0.00257625, 'DA2': 0.0014637500000000002, 'DB2': 0.0014637500000000002}
    
    print("service times:", sts)
    
    return sts

def serviceDemands(service_times:dict, relative_visit_ratios:dict):
    
    service_demands={} # V_i * u_i
    
    
    service_demands["B1"]=relative_visit_ratios["B1"]*service_times["B1"]
    service_demands["DA1"]=relative_visit_ratios["DA1"]*service_times["DA1"]
    service_demands["DB1"]=relative_visit_ratios["DB1"]*service_times["DB1"]
    
    service_demands["B2"]=relative_visit_ratios["B2"]*service_times["B2"]
    service_demands["DA2"]=relative_visit_ratios["DA2"]*service_times["DA2"]
    service_demands["DB2"]=relative_visit_ratios["DB2"]*service_times["DB2"]
    
    #service_demands["T1"]=relative_visit_ratios[T1]*1000
    
    print("service demands:", service_demands)
    
    bottleneck=max(service_demands, key= lambda x: service_demands[x])
    
    print("bottleneck:", bottleneck)
    
    return service_demands, bottleneck

def NOpt(service_demands:dict, thinking_time:float, bottleneck:str):
    
    n_opt=(sum(service_demands.values())+thinking_time)/service_demands[bottleneck]
    
    print("n_opt:",n_opt)
    
    return n_opt

def bounds_getter_printer():
    
    relative_visit_ratios=trafficEqSolverOpt1()
    service_times=service_time()

    service_demands, bottleneck=serviceDemands(service_times, relative_visit_ratios)
    
    n_optimal = NOpt(service_demands, thinking_time=1, bottleneck=bottleneck)
    lb = lower_bound(service_demands, max_n_users=800, thinking_time=1, bottleneck=bottleneck)
    ub = upper_bound(service_demands, max_n_users=800, thinking_time=1, bottleneck=bottleneck)
    
    return lb, ub, n_optimal

def theoretical_plots_opt():
    users, X, R, _=MVA_data_reader("MVA/MVA.jmva")

    marker='*'
    lb, ub, n_optimal = bounds_getter_printer()

    fig, ax= plt.subplots(figsize=(8, 6))

    ax.plot(users, X, label="$X$")
    ax.plot([x[0] for x in ub[1]], [min(ub[0],x[1]) for x in ub[1]],label="$\min\left(\\frac{N}{{D}+{\overline{Z}}}, \\frac{1}{D_{b}}\\right)$", linestyle='dotted', color='red')

    stem=ax.scatter(n_optimal, ub[0], label="$N_{opt}$", marker=marker)

    ax.legend(fontsize=12)
    ax.grid()
    ax.set_title("Empirical throughput (MVA) vs Number of users \n with theoretical bounds")
    ax.set_xlabel("$N$")
    ax.set_ylabel("$X$")

    fig, ax= plt.subplots(figsize=(8, 6))

    ax.plot(users, R, label="$\overline{R}$")
    ax.plot([x[0] for x in lb[1]], [max(lb[0], x[1]) for x in lb[1]],label="$\max(D, {N \cdot D_{b}}-\overline{Z})$", linestyle='dotted', color='red')

    stem=ax.scatter(n_optimal, lb[0], label="N_{opt}", marker=marker)

    ax.legend(fontsize=12)
    ax.grid()
    ax.set_title("Empirical expected response time (MVA) vs Number of users \n with theoretical bounds")
    ax.set_xlabel("$N$")
    ax.set_ylabel("$\overline{R}$")

    plt.show()
    
def utilization_plot():
    users, _, _, U = MVA_data_reader("MVA/MVA.jmva")
    
    fig, ax= plt.subplots(figsize=(8, 6))
    
    stations=U[0].keys()
    
    for station in stations:
        
        if station=="DB1" or station=="DB2":
            continue
        
        if station=="DA1":
            l="$\\rho_{"+station+"}$, $\\rho_{"+"DB1"+"}$"
        else:
            if station=="DA2":
                l="$\\rho_{"+station+"}$, $\\rho_{"+"DB2"+"}$"
            else:
                l="$\\rho_{"+station+"}$"
                
        #    line="-"
        #else:
        #    line=(0, (5, 5))
            
        ax.plot(users, [u_station[station] for u_station in U], label=l)
    
    ax.legend(fontsize=12)
    ax.grid()
    ax.set_title("Utilization vs Number of users")
    ax.set_xlabel("$N$")
    ax.set_ylabel("$\\rho$")
    
    plt.show()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Utility script to perform DB operations',formatter_class=argparse.RawTextHelpFormatter)
    
    action_group=parser.add_argument_group('Action to perform (choose one)')
    action_group=action_group.add_mutually_exclusive_group(required=True)
    
    action_group.add_argument('--mva_plots', action='store_true', help='Create MVA plots with theoretical bounds')
    action_group.add_argument('--utilization_plot', action='store_true', help='Create Utilization plot')
    
    args = parser.parse_args()
    
    if "mva_plots" in args and args.mva_plots:
        print("\n\nMVA plots:\n")
        theoretical_plots_opt()
    if "utilization_plot" in args and args.utilization_plot:
        print("\nUtilization plot:\n")
        utilization_plot()