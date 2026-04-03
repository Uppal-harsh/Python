lst = ["a","ab","abb","abc","b","adcb","abbb","adas","f","hg","eeee"]
a = {}
for i in range(len(lst)):
    x = len(lst[i])
    if x not in a:
        a[x] = []
        a[x].append(lst[i])
    else:
        a[x].append(lst[i])
print(a)

