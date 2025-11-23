a = True
b = True
c = True


if (a and b and (not c)) or (b and c and (not a)) or (a and c and (not b)):
    print("+ve")
else:
    print("-ve")
