#create a dictionary based upon the starting values of the pair and print the string with maximum character
max_val = 0
max_len = 0
D = {'a':'apple', 'b':'banana', 'c':'chocolate', 'd':'dog'}
for i in D:
    if len(D[i])>max_len:
        max_len = len(D[i])
        max_val = D[i]
print(max_val)
