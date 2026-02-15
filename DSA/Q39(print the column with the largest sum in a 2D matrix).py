a = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
b = []
def column_sum(x, y):
    num_columns = len(x[0])
    for j in range(num_columns):
        total = 0
        for i in range(len(x)):
            total = total + x[i][j]
        y.append(total)
    return y

p = column_sum(a,b)
print(p.index(max(p)))







