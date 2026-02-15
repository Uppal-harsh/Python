a = [[1,2,3],[4,15,6],[7,8,9]]
b = []
def coord_max(x,coord):
    maxi = 1
    coord = []
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] > maxi:
                maxi = x[i][j]
                coord = [i,j]
    return coord, maxi

print(coord_max(a,b))

