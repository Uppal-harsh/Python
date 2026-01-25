a = []

for i in range(5):
    num = int(input("enter number: "))
    a.append(num)

a.sort()
print(a)

for i in range(len(a)):
    if a[i] % 2 != 0:
        print("the smallest odd number is ", a[i])
        break

for i in range(len(a) - 1, -1, -1):
    if a[i] % 2 == 0:
        print("the largest even number is ", a[i])
        break