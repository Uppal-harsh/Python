a = int(input("enter number 1:"))
b = int(input("enter number 2:"))
c = int(input("enter number 3:"))
d = int(input("enter number 4:"))

if a>b:
    if a>c:
        if a>d:
            print("the largest number is: ", a)
        else:
            print("the largest number is: ", d)
    else:
        if c>d:
            print("the largest number is: ", c)
        else:
            print("the largest number is: ", d)
else:
    if b>c:
        if b>d:
            print("the largest number is: ", b)
        else:
            print("the largest number is: ", d)
    else:
        if c>d:
            print("the largest number is: ", c)
        else:
            print("the largest number is: ", d)

