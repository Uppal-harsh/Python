a = [[1,2,3],
     [4,5,6],
     [7,8,9]]
def diagonal(p):
    for i in range(len(a)):
        print(a[i][i])
        a[i].reverse()
    print("\n")
    for i in range(len(a)):
        print(a[i][i])
    return p
diagonal(a)
