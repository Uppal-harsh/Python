a = int(input("enter number: "))
g = 5

for i in range(10000):

    if a == g:
        print("you guessed the number")
        break
    a = int (input("try again: "))
