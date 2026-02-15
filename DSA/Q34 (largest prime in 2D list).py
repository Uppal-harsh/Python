x = [[4,2,7,4],[19,17,7,3,23]]
d = []

def checkprime(a):
    p = True
    for val in a:
        for i in range(2, (val//2) + 1):
            if val % i == 0:
                p = False
    return p

for t in range(len(x)):
    if checkprime(x[t]):
        d.append(x[t])
print("the max prime number is", max(max(d)))

