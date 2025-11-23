a = int(input("enter starting point: "))
b = int(input("enter ending point: "))
c = int(input("enter multiple: "))

i=a
while i<b:
    if i%c==0:
        print(i)
    i = i+1
