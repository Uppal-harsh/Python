n = int(input("enter"))
for i in range(n):
    for j in range(n-i):
        if j<(n-i):
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print("")
