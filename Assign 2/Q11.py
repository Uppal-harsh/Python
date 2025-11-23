n = int(input("Enter number of terms you want in the fibbonacci sequence: "))
a = 0
b = 1
i = 0

while i < n:
    print(a)
    a = b
    b = a + b
    i = i + 1
