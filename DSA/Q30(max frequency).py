a = [1,5,3,2,7]
b = [4,1,8,5,3]
c = [1,7,3,3]
d = [a,b,c]
e = []
for i in d:
    for j in i:
        e.append(j)
    e.extend(i)
e.sort()
print(e)