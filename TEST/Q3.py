a = int(input("enter number 1:"))

if a%3==0 and a%7==0:
    print("the number is a multiple of 3 and 7")
elif a%7==0:
    print("the number is a multiple of 7")
elif a%3==0:
    print("the number is a multiple of 3")
else:
    print("the number is invalid")
