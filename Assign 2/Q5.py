x = int(input("enter a number: "))
i = x
count = 0

while i > 0:
    i = i//10
    count = count + 1
print("the number of digits are: ", count)