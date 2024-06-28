import json
import matplotlib.pyplot as plt

import os

def load_test_reader():
    script_path=os.path.dirname(os.path.abspath(__file__))

    X = []
    R = []
    users = range(50, 550, 50)

    for n_users in users:
        with open(f"{script_path}/results_{n_users}/statistics.json", "r") as f:
            results = json.load(f)
            
            X.append(results["Transaction Controller"]["throughput"])
            R.append(results["Transaction Controller"]["meanResTime"]/1000)

    print(X)
    print(R)
    
    return users, X, R

def load_test_graphs(users, X, R):
    
    fig, axs = plt.subplots(
        nrows=1, ncols=2, figsize=(8, 6)
    )

    axs[0].plot(users, X, label="Throughput")
    axs[0].set_title("Throughput")

    axs[1].plot(users, R, label="Mean Response Time")
    axs[1].set_title("Mean Response Time")

    plt.show()
    
if __name__ == "__main__":
    users, X, R = load_test_reader()
    load_test_graphs(users, X, R)