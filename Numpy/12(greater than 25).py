import numpy as np

a = np.array([10,26,13,16,37,29])
b = np.where(a>25)
print(a[b])