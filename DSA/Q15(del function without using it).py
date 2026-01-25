a = [2, 6, 2, 5, 7, 9, 4, 2, 4, 6]
x = int(input("Enter the number you want to delete: "))

b = [0] * len(a)
count = 0
for i in range(len(a)):
    if a[i] != x:
        b[count] = a[i]
        count = count + 1
b = b[:count]
print(b)