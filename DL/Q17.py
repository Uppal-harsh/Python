total = int(input("Enter the billing amount: "))
customer_card = str(input("do you have the special customer card?  "))

if total > 2000:
    if customer_card == "yes":
        discount_1 = 3
        discount_2 = 5
        total_1 = total - total * ((discount_1 + discount_2) / 100)
        print("the billing amount is: ", total_1)
    else:
        discount_1 = 3
        total_1 = total - total * (discount_1 / 100)
        print("the billing amount is: ", total_1)
else:
    if customer_card == "yes":
        discount_1 = 5
        total_1 = total - total * (discount_1 / 100)
        print("the billing amount is: ", total_1)
    else:
        discount_1 = 0
        total_1 = total - total * (discount_1 / 100)
        print("the billing amount is: ", total_1)
