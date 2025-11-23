num = int(input("enter number: "))
x=0

while num!=0:
    n = num%10
    x = x*10 + n
    num = num//10
print(x)





