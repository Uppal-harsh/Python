a = [[1,2,3],
     [4,5,6],
     [7,8,9]]
b = []
def transpose(x,y):
    for i in range(len(x)):
        for j in range(len(x[i])):
            y.append(x[j][i])
    return y

print(transpose(a,b))
