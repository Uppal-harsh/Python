a = int(input("enter number 1: "))
b = int(input("enter number 2: "))
c = int(input("enter number 3: "))

if a>b:
    if a>c:
        h=a
        s1=b
        s2=c
    else:
        h=c
        s1=a
        s2=b
else:
    if b>c:
        h=b
        s1=a
        s2=c
    else:
        h=c
        s1=a
        s2=b

if (h**2) == (s1**2) + (s2**2):
    print("the triangle is a right triangle")
else:
    print("the triangle is not a right triangle")