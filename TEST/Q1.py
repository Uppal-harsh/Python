a = int(input("Enter number 1 : "))
b = int(input("Enter number 2 : "))
c = int(input("Enter number 3 : "))
d = int(input("Enter number 4 : "))

if a > b and a > c and a > d:
    if b > c and b > d:
        print(b, "is the second greatest number")
    elif c > b and c > d:
        print(c, "is the second greatest number")
    else:
        print(d, "is the second greatest number")
elif b > a and b > c and b > d:
    if a > c and a > d:
        print(a, "is the second greatest number")
    elif c > a and c > d:
        print(c, "is the second greatest number")
    else:
        print(d, "is the second greatest number")
elif c > a and c > b and c > d:
    if a > b and a > d:
        print(a, "is the second greatest number")
    elif b > a and b > d:
        print(b, "is the second greatest number")
    else:
        print(d, "is the second greatest number")
else:
    if a > b and a > c:
        print(a, "is the second greatest number")
    elif b > a and b > c:
        print(b, "is the second greatest number")
    else:
        print(c, "is the second greatest number")