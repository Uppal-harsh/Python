a = int(input("enter side length one: "))
b = int(input("enter side length two: "))
c = int(input("enter side length three: "))

if a==b==c:
    print("the triangle is a equilateral triangle")
elif a==b or a==c or b==c:
    print("the triangle is isosceles")
else:
    print("the triangle is scalene")
