x = int(input("enter a number: "))
i = x
p = 0
s = 0
while x > 0:
    i = i%10
    s = i//10
    p = p + i
print(p)
print(s)



