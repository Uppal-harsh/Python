d = [[1,5,3,2,7],[4,1,8,5,3],[1,7,3]]
e = []
for i in d:
    p = sum(i)
    e.append(p)
print(max(e), "is the sum of the list", e.index(max(e))+1)

