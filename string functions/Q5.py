a = 'hello my name is harsh'
b = {}

for i in a:
    c = a.count(i)
    if c in b:
        continue
    else:
        b.update({i:c})
print(b)


