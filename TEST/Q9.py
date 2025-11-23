a = True
b = False
c = True
count = 0
if a:
    count +=1
if b:
    count +=1
if c:
    count +=1
if count==1 or count==3:
    print("the number is valid")
else:
    print("the number is not valid")