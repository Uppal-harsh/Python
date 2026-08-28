import numpy as np

a = np.array([1,2,3,5,6,7,8,9,10,11,12,13])
for i in range(len(a)):
    if a[i]>10:
        a[i] = 10

print(a)