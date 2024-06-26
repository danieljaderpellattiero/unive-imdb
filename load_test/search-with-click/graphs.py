from tqdm import tqdm
import json
import matplotlib.pyplot as plt

X = []
R = []
users = range(50, 550, 50)

for n_users in users:
    with open(f"results_{n_users}/statistics.json", "r") as f:
        results = json.load(f)
        
        X.append(results["Total"]["throughput"])
        R.append(results["Total"]["meanResTime"]/1000)

print(X)
print(R)
fig, axs = plt.subplots(
    nrows=1, ncols=2, figsize=(8, 6)
)

axs[0].plot(users, X, label="Throughput")
axs[0].set_title("Throughput")

axs[1].plot(users, R, label="Mean Response Time")
axs[1].set_title("Mean Response Time")

plt.show()