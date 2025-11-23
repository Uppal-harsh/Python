a = int(input("enter number 1:"))
b = int(input("enter number 2:"))
c = int(input("enter number 3:"))

if a>b:
    if a>c:
        if b>c:
            print("the second largest number is :", b)
        else:
            print("the second largest number is :", c)
    else:
        print("the second largest number is :", a)
else:
    if b>c:
        if c>a:
            print("the second largest number is :", c)
        else:
            print("the second largest number is :", a)
    else:
        print("the second largest number is :", b)
