r = int(input())
c = int(input())
for i in range (1,r+1):
    for j in range(c):
        if i%2==0:
            if j % 2 != 0:
                print(1, end=' ')
            else:
                print(0, end=' ')
        else:
            if j % 2 == 0:
                print(1, end=' ')
            else:
                print(0, end=' ')
    print("")