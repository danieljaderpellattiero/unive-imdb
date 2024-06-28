from eqSolver import trafficEqSolver, serviceDemands, NOpt, lower_bound, upper_bound
from service_times import service_times_reader
from load_test.search_with_click.load_test_reader import load_test_reader

import matplotlib.pyplot as plt


def load_test_graphs_with_bounds():
    
    relative_visit_ratios=trafficEqSolver()
    service_times = service_times_reader(n_cores=8)
    service_demands, bottleneck = serviceDemands(relative_visit_ratios, service_times)

    n_optimal = NOpt(service_demands, thinking_time=1, bottleneck=bottleneck)
    lb = lower_bound(service_demands, max_n_users=500, thinking_time=1, bottleneck=bottleneck)
    ub = upper_bound(service_demands, max_n_users=500, thinking_time=1, bottleneck=bottleneck)


    users, X, R = load_test_reader()
    
    
    fig, axs = plt.subplots(
        nrows=1, ncols=2, figsize=(8, 6)
    )

    axs[0].plot(users, X, label="Throughput")
    axs[0].plot([x[0] for x in ub[1]], [min(ub[0],x[1]) for x in ub[1]],label="upper bound")
    axs[0].set_title("Throughput")

    axs[1].plot(users, R, label="Expected Response Time")
    axs[1].plot([x[0] for x in lb[1]], [max(lb[0], x[1]) for x in lb[1]],label="lower bound")
    axs[1].set_title("Expected Response Time")

    plt.show()
    
load_test_graphs_with_bounds()

