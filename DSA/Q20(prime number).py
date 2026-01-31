a = []
b = []
for p in range(5):
    x = int(input("Enter number: "))
    a.append(x)
prime = False
count = 0
for i in range(len(a)):
    for j in range(2,a[i]):
        if a[i] % j == 0:
            prime = False
            count += 1
            break
    if count == 0 and a[i] > 1:
        prime = True
    if prime:
        b.append(a[i])
print("prime found: ", b)

'''a = int(input("enter number : "))
prime = False
count = 0
for i in range(2, a):
    if a % i == 0:
        prime = False
        count +=1
    else:
        prime = True
if count > 1:
    print("not prime number")
else:
    print("prime number")'''