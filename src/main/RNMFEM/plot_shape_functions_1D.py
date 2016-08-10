import numpy as np
import matplotlib.pyplot as plt

u = np.arange(-1.0, 1.1, 0.1)

def f1 (u):
	return -u*(1.0-u)/2.0
def f2 (u):
	return (1.0-u*u)
def f3 (u):
	return u*(1.0+u)/2.0

plt.plot(u, f1(u),u, f2(u),u, f3(u))
plt.show()

u=0.57
print f1(u)+f2(u)+ f3(u)