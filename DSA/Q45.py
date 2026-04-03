#sort words in dict as keys for the first alphabet and value as words

lst = ["apple","banana","orange","guava","cat","dog"]
a = {}
for i in range(len(lst)):
    x = (lst[i][0])
    if x not in a:
        a[x] = []
        a[x].append(lst[i])
    else:
        a[x].append(lst[i])
print(a)
