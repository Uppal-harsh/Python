a = [2,6,2,5,7,9,4,2,4,6]
x = int(input("enter the number you want to delete in the function"))

for i in range(len(a)):
    if a[i] == x:
        a[i] = a[i+1]
        continue

print(a)
print(len(a))

