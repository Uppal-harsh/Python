amount = int(input("enter billing amount: "))
card = str(input("do you have a credit card?"))
if amount>5000:
    discount = 20
elif 2000<amount<5000:
    discount = 10
elif card == "yes":
    discount = 5
else:
    discount = 0

total_amount = amount - (discount * amount)/100
print("your billing amount is: ", amount)
print("total amount:",total_amount)

