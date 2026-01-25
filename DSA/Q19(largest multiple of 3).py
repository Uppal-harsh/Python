a = []

for i in range(5):
    num = int(input("enter number: "))
    a.append(num)
a.sort()
for i in range(len(a)-1,-1,-1):
    if a[i] % 3 == 0:
        print("the largest multiple of 3 is ", a[i])
        break
