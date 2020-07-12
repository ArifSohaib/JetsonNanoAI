import matplotlib.pyplot as plt
import numpy as np


x2 = np.arange(-4,4,0.1)
x = np.linspace(0,2*np.pi,100)
y = np.cos(x)
z = np.sin(x)
y2 = np.tan(x)
plt.grid(True)
plt.xlabel("my x values")
plt.ylabel("my y values")
plt.title("my first graph")
plt.plot(x,y,'b:o',linewidth=3,label="blue line")
plt.plot(x,z,'r:^',linewidth=2, label="red line")
plt.plot(x,y2,'g-',linewidth=2, label="green line")
plt.legend(loc="upper center")
#plt.axis([0,5,0,10])y2
plt.show()