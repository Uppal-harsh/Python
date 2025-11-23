a = int(input("enter number 1: "))
b = int(input("enter number 2: "))
c = int(input("enter number 3: "))

if a>b and a>c:
    if a%2==0:
        print(a)
    else:
        if b>c:
            if b%2==0:
                print(b)
            else:
                if c%2==0:
                    print(c)
                else:
                    print("null")
        else:
            if c%2==0:
                print(c)
            else:
                if b%2==0:
                    print(b)

                else:
                    print("null")

elif b>c and b>a:
    if b%2==0:
        print(b)
    else:
        if a>c:
            if a%2==0:
                print(b)
            else:
                if c%2==0:
                    print(c)
                else:
                    print("null")
        else:
            if c%2==0:
                print(c)
            else:
                if a%2==0:
                    print(a)
                else:
                    print("null")

else:
    if c%2==0:
        print(c)
    else:
        if a>b:
            if a%2==0:
                print(a)
            else:
                if b%2==0:
                    print(b)
                else:
                    print("null")
        else:
            if b%2==0:
                print(b)
            else:
                if c%2==0:
                    print(c)
                else:
                    print("null")

