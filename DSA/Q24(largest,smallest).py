a = []
b = []
for i in range(8):
    num = int(input("enter number: "))
    a.append(num)
a.sort()
for i in range(len(a)//2):
    b.append(a[len(a) - i-1])
    b.append(a[i])

print(b)







