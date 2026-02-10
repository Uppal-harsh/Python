a = [20,10,30,50,100]
for i in range(len(a)):
    for j in range(len(a)-i-1):
        if a[j]>a[j+1]:
            a[j],a[j+1] = a[j+1],a[j]
print(a)








