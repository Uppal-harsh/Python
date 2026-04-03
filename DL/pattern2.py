r = int(input())
c = int(input())
t = "a"
for i in range (1, r+1):
    for j in range (i):
        print(t, end=" ")
        if t=="a":
            t="b"
        elif t=="b":
            t="c"
        else:
            t="a"
    print()