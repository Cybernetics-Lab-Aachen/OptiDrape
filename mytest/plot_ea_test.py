import pickle
import matplotlib as mp
import numpy as np
from Data.fit_data import *
import matplotlib.pyplot as plt

iter_500 = pickle.load(open("./k_sum_stat_1000.p", "rb"))

print(iter_500)

print(iter_500)
iter_500_sorted_population = []
iter_500_pop_ave = []
iter_500_var = []

for iter in range(len(iter_500)):
    iter_500_sorted_population.append(sorted(iter_500[iter][0], reverse=True))
    iter_500_pop_ave.append(np.min(iter_500[iter][0]))
    #iter_500_pop_ave.append(np.sqrt(np.std(iter_500[iter][0])))

print(iter_500_sorted_population)
print(iter_500_pop_ave)
fig = plt.figure(figsize=(50, 5))

ax = fig.add_subplot(111)


iter_500_pop_ave = np.asarray(iter_500_pop_ave)
iter_500_pop_ave = 1 / iter_500_pop_ave
iter_500_pop_ave = iter_500_pop_ave / iter_500_pop_ave.max()

iter_500_pop_ave = iter_500_pop_ave / 0.02
iter_500_pop_ave = iter_500_pop_ave.tolist()

_data_reg_func = fitted_data_func(fit_data(x=list(range(len(iter_500_pop_ave))), y=iter_500_pop_ave, deg=2))

ax.plot(np.arange(1000), iter_500_pop_ave, 'bo', label="Maximal fitness score in each population")
ax.plot( np.arange(1000), _data_reg_func(np.arange(1000)), 'r-', label="Approximation of maximal fitness score")
plt.axis([0, 1000, min(iter_500_pop_ave), 1])
plt.grid(True, linewidth=1)
plt.xlabel('Iteration')
plt.ylabel('Normalized fitness score')

legend = ax.legend(loc='upper right', shadow=True)

ax.set_xticks(np.arange(0, 1001, 30))

plt.show()

fig.savefig("graph1000_var.png", dpi=600)
input()

print("test")




