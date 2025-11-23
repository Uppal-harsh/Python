num = int(input("enter number: "))
x=0
i = num
while i!=0:
    n = i%10
    x = x*10 + n
    i = i//10
if num == x:
    print("this number is a palindrome")
else:
    print("this number is not a palindrome")

