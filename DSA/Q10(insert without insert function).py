a = [7,4,9,2,1,3,9]
x = int(input("enter index of the number you want to add to: "))
y = int(input("enter number you want to add: "))

for i in a:
    a[x+1] = a[x]
a[x] = y
print(a)


