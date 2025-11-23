a = int(input("enter the buying price: "))
b = int(input("enter the selling price: "))

if a>b:
    print("it was a loss")
    c=a-b
    print("the amount of loss is: ", c)
else:
    print("it was a profit")
    c=b-a
    print("the amount of profit is: ", c)
