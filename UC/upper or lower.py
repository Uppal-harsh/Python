import random

a = int(input("enter the range you want to play this game in: "))
bot_guess = random.randint(1,a)
again = True
while again:
    guessed_number = int(input("enter number you want to guess"))
    if guessed_number > bot_guess:
        print(f"your number is less than {guessed_number}")
        again = True
    elif guessed_number < bot_guess:
        print(f"your number is greater than {guessed_number}")
        again = True
    elif guessed_number == bot_guess:
        print("you guessed right-you win!")
        break
    else:
        print("enter a valid number")



