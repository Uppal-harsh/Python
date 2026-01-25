#list all prime numbers in a given list
a = []
count = 0
for i in range(5):
    x = int(input("enter number: "))
    a.append(x)
for i in range(2,max(a)+1):
    for j in range(2,i):
        if(i%j==0):
            break
    else:
        print(i,"is a prime number")
        count = count + 1


