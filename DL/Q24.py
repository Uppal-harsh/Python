a = int(input("enter marks of maths out of 100: "))
b = int(input("enter marks of science out of 100: "))
c = int(input("enter marks of english out of 100: "))
d = int(input("enter marks of sst out of 100: "))
e = int(input("enter marks of hindi out of 100: "))

total_marks = 500
obtained_marks = a+b+c+d+e
percent = (obtained_marks/total_marks)*100
if percent<61:
    grade = 'F'
elif percent<71:
    grade = 'D'
elif percent<81:
    grade = 'C'
elif percent<91:
    grade = 'B'
else:
    grade = 'A'
print("your overall grade is: ", grade)
print("your percentage is", percent, '%')

