a = int(input("enter temperature: "))

if a<0:
    print("Freezing\n")
elif a<16:
    print("Cold\n")
elif a<26:
    print("Pleasant\n")
elif a<35:
    print("Warm\n")
else:
    print("Hot\n")

if a%5==0:
    print("Special day")
