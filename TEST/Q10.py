a = int(input("enter number 1: "))
b = int(input("enter number 2: "))
c = int(input("enter number 3: "))
d = int(input("enter number 4: "))
e = int(input("enter number 5: "))
count = 0

if a%2!=0:
    a1 = 0
else:
    a1 = a
    count += 1
if b%2!=0:
    b1 = 0
else:
    b1 = b
    count += 1
if c%2!=0:
    c1 = 0
else:
    c1 = c
    count += 1
if d%2!=0:
    d1 = 0
else:
    d1 = d
    count += 1
if e%2!=0:
    e1 = 0
else:
    e1 = e
    count += 1
average = (a1+b1+c1+d1+e1)/count
print(average)
