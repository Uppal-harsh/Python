a = [1,5,3,2,7]
b = [4,1,8,5,3]
c = [1,7,3]

d = [a,b,c]

for i in d:
    for j in i:
        print(j, end=" ")
print("\n")
for i in range(len(d)):
    for j in range(len(d[i])):
        print(d[i][j], end=" ")
