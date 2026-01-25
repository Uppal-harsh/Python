a = [2,5,8,4,2,2,6,8,2]

x = int(input("Enter number to find index: "))

found_num = 0

for i in range(len(a)):
    if a[i] == x:
        found_num = i
        break

print("Index:", found_num)
