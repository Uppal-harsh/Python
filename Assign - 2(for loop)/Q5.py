a = int(input("enter number: "))
count = 0
for i in range(a):
    a = a//10
    count+=1
    if a==0:
        break
print(count)