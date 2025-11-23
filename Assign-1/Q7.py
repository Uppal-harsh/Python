a = int(input("enter a number: "))

if a%2==0 and a<20:
        print("Small even")
elif a%2!=0 and 20<a<50:
    print("Weird odd")
elif a%5==0 and a>50:
    print("Big multiple of 5")
else:
    print("not valid")
