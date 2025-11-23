a = int(input("enter a number: "))

if a % 3 == 0 and a % 5 == 0 and a % 2 != 0:
    print("the number is valid")
else:
    print("the number is not valid")