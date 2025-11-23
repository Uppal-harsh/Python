a = int(input("Enter your electricity unit: "))

n1 = 15
n2 = 25
n3 = 38


if a<=n1:
    x = (a*3)
elif a<=n2:
    b = a-n1
    x = (15*3) + (b*5)
elif a<=n3:
    b = a-n2
    x = (15*3) + (10*5) + (b*7)
else:
    b = a-n3
    x = (15*3) + (10*5) + (12*7) + (b*9)

print(x)