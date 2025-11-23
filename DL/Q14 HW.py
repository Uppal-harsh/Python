a = int(input("enter number 1:"))
b = int(input("enter number 2:"))
c = int(input("enter number 3:"))


if a>c:
    if a>b:
        print("the largest number is:", a)
    else:
        print("the largest number is:", b)
else:
    if c>b:
        print("the largest number is:", c)
    else:
        print("the largest number is:", b)