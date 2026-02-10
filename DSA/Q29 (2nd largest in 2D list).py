a = [1,5,2,4]
b = [2,3,6,4]
c = [2,3,4,9]
d = [a,b,c]
e = []
for i in d:
    for j in i:
        e.append(j)
e.sort(reverse=True)
print(e)
print(e[1])

