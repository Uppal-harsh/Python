n = int(input("how many numbers do you want in the fibonacci series: "))

a = 0
b = 1
c = 0

for i in range(1, n+1):
    print(a)
    c = a + b
    a=b
    b=c
