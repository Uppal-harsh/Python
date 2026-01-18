num = [1,2,3,4,5,6,7,8,9]

mini = num[0]
for i in range(0,8):
    if num[i] < mini:
        mini = num[i]
print(mini)
