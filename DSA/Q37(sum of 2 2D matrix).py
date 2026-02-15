a1 = [[1,3,3],
      [3,6,7],
      [3,1,7]]

a2 = [[1,3,3],
      [3,6,7],
      [3,1,7]]
a3 = []
def sum_matrix(a,b,c):
    for i in range(len(a)):
        for j in range(len(a[i])):
            x = a[i][j] + b[i][j]
            c.append(x)
    return c
print(sum_matrix(a1,a2,a3))

