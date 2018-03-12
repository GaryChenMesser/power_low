import powerlaw
import networkx as nx
import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math

G = nx.read_edgelist(sys.argv[1])
data = sorted([d for n, d in G.degree()]) # data can be list or numpy array
print(len(data))

results = powerlaw.Fit(data)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')

y = []
x = []

for a in data:
	temp = int(math.log(a))
	if temp in x:
		y[x.index(temp)] += 1
	else:
		x.append(temp)
		y.append(1)

for i in range(len(y)):
	y[i] /= len(data)

x0 = []
y0 = []
step = 1 / len(data)

for a in data:
	temp = round(math.log(a), 2)
	if temp in x0:
		y0[x0.index(temp)] -= step
	else:
		x0.append(temp)
		if len(x0) == 1:
			y0.append(1.)
		else:
			y0.append(y0[len(x0) - 2])

print(x0)	
print(y0)

x1 = [i for i in range(len(x))]
y1 = [math.exp(- (results.power_law.alpha-1) * i) for i in range(len(x))]

plt.plot(x, y,'bo')
plt.plot(x0, y0, 'ro')
plt.plot(x1, y1)
#plt.xscale('log')
plt.yscale('log')
#plt.show()
plt.savefig(sys.argv[1].split('/')[-1].split(',')[0] + '.png')

