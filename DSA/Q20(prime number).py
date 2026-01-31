n = []
m = []

for x in range(5):
    p = int(input("enter number for the list: "))
    n.append(p)

for val in n:
    is_prime = True
    for j in range(2, (val // 2) + 1):
        if val % j == 0:
            is_prime = False
            break
    if is_prime:
        m.append(val)
print("Prime:", m)