n = int(input("enter"))
for i in range(n+1):
    for j in range(n+1):
        if j<(n-i):
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print("")
