a = int(input("enter number : "))
prime = True

for i in range(2,a):

    if a%i == 0:
        prime = False
        break
if prime:
    print("num is a prime number")
else:
    print("num is not a prime number")