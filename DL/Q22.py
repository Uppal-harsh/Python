amount = int(input("enter your amount: "))
if amount < 2000:
    discount = 3
elif amount < 4000:
    discount = 5
elif amount < 6000:
    discount = 8
else:
    discount = 10

total_amount = amount - (amount*discount)/100
print("your billing amount is :", amount)
print("your total viable discount is :", discount, "%")
print("your total payable amount is :", total_amount)