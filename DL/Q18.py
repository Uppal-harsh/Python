a = int(input("enter a number:"))
if a%2 == 0:
    if a>0:
        print("the number is even and positive")
    else:
        print("the number is even and negative")
else:
    if a<0:
        print("the number is odd and negative")
    else:
        print("the number is odd and positive")