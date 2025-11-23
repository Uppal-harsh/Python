#automorphic number
num = int(input("enter number: "))
square = num ** 2
i=0
count = 0
p = num
while p>0:
    i= p%10
    count += 1
    p = p//10
print(count)
print("the square of the number is : ", square)

m = square%(10**count)
print(m)
if m == num:
    print("the number is an automorphic number")
else:
    print("no the number is not an automorphic number")






