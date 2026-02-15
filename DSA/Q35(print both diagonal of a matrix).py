a = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
b = []
c = []
def diagonal(p, q, r):
    n = len(p)
    for i in range(n):
        q.append(p[i][i])
        r.append(p[i][n-i-1])
    return q, r
print(diagonal(a, b, c))
