print("rock = 1, paper = 2, scissors = 3")
a1 = int(input("player 1 input: "))
a2 = int(input("player 2 input: "))


r = 1
p = 2
s = 3

if a1==a2:
    print("DRAW")
elif (a1==r and a2==p) or (a1==p and a2==s) or (a1==r and a2==s):
    print("player 2 wins!")
elif (a1==p and a2==r) or (a1==s and a2==p) or (a1==s and a2==r):
    print("player 1 wins!")
else:
    print("invalid input")