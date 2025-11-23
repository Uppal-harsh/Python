a = float(input("enter x coordinate"))
b = float(input("enter y coordinate"))

if -1.5<a<1.5 and -1.5<b<1.5:
    print("inside")
elif (a==1.5 and b==1.5) or (a==1.5 and b==-1.5) or (a==-1.5 and b==1.5) or (a==-1.5 and b==-1.5):
    print("boundary")
else:
    print("outside")

