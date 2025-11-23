a=1
i=a
s=0
while i>0 or i<=0:
    i = int(input("enter a number:"))
    s = s+i

    if i>0:
        print("the number is positive")
    else:
        print("the number is negative")
        print("the sum of numbers till now is : ", s)

