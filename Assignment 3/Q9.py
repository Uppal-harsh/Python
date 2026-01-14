m = int(input("Enter a number: "))
for i in range(m):
    for j in range(m):
        if i==0 or j==0 or i==m-1 or j==m-1:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print()