a = []
b = []

for i in range(5):
    x = int(input("enter number: "))
    a.append(x)

for num in a:
    while num >= 10:
        m = num // 10
        n = num % 10
        num = m + n
    b.append(num)
p = sum(b)
print(b)
print(p)
