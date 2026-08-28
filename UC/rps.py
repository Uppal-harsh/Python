import random

print("lets play rock paper and scissors")
choice = ["rock", "paper", "scissor"]
choice_out = random.choice(choice)
again = True

while again:
    a = (input("choose from rock paper and scissor: "))
    b = random.choice(choice)
    if a == b:
        win = True
        print("its a tie")
    elif a == "rock" and b == "paper":
        win = False
        print(f"the bot chose {b} but you chose {a}, you lose")
    elif a == "scissor" and b == "rock":
        win = False
        print(f"the bot chose {b} but you chose {a}, you lose")
    elif a == "paper" and b == "scissor":
        win = False
        print(f"the bot chose {b} but you chose {a}, you lose")
    elif a == "scissor" and b == "paper":
        win = True
        print(f"the bot chose {b} but you chose {a}, you win")
    elif a == "rock" and b == "scissor":
        win = True
        print(f"the bot chose {b} but you chose {a}, you win")
    elif a == "paper" and b == "rock":
        win = True
        print(f"the bot chose {b} but you chose {a}, you lose")
    elif a == "scissor" and b == "paper":
        win = True
        print(f"the bot chose {b} but you chose {a}, you win")
    else:
        print("invalid choice")
    inp = input("play again? y/n: ")
    if inp.lower() == "y":
        again = True
    elif inp.lower() == "n":
        again = False
    else:
        print("invalid choice")