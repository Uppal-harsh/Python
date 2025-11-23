n = int(input("enter limit of the sequence: "))
m = int(input("enter how many times you want to repeat the sequence: "))

for i in range(m+1):
    for j in range(n+1):
        print(i,",",j, end = "    ")
    print("")

