a = int(input("enter number 1-50: "))
if a%3==0 and a%5==0:
    print("FIZZBIZZ")
elif a%3==0:
    print("FIZZ")
elif a%5==0:
    print("BIZZ")
else:
    print(a)