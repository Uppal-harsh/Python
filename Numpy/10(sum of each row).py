import numpy as np

a = np.arange(9)
a = np.reshape(a,(3,3))
b = np.sum(a[0])
print(b)