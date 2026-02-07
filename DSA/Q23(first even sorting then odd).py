a = [1,2,4,5,6,12,57,23,14]
n = []
m = []

for i in range(len(a)):
    if a[i] % 2 == 0:
        n.append(a[i])
    else:
        m.append(a[i])
n.sort()
m.sort()
q = n+m
print(q)