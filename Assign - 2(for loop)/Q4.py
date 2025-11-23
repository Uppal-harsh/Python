#reverse number
num = int(input("Enter a number: "))
x=0
for i in range(num):
    digit = num % 10
    x = x * 10 + digit
    num = num // 10
    if num == 0:
        break
print(x)