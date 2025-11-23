a = int(input("enter x coordinate: "))
b = int(input("enter y coordinate: "))

if a>0 and b>0:
    print("the point is in 1st quadrant")
elif a>0 and b<0:
    print("the point is in 2nd quadrant")
elif a<0 and b>0:
    print("the point is in 3rd quadrant")
else:
    print("the point is in 4th quadrant")
