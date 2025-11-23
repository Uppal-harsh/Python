a = int (input("Enter a number: "))
x = 0
rev = a
for i in range (rev):
    n = rev%10
    x = x*10 + n
    rev = rev//10
    if rev == 0:
        break
print(x)

if x == a:
    print("the number is a palindrome")
else:
    print("the number is not a palindrome")
