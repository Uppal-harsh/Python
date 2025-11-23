user = str(input("enter your name: "))
o = 0
bal = 10000
new_bal = bal
print("welcome", user, "thanks for accessing our ATM")
while o!=4:
    print("choose options: \n1. withdraw \n2. deposit \n3. check balance \n4. exit")
    o = int(input("enter your choice: "))
    if o==1:
        w = int(input("enter the amount you want to withdraw: "))
        bal -= w
        if bal>0:
            print("balance is", bal)
        else:
            print("the withdrawal cannot be more than the balance")
    elif o==2:
        w = int(input("enter the amount you want to deposit: "))
        bal += w
        print("balance is", bal)
    elif o==3:
        print(bal)
    else:
        break
