a = int(input("enter number:"))
for i in range(a):
    for j in range(a-i):
        print(a-j, end=" ")
    print("")
