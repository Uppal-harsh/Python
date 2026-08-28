import random

letters = "abcdefgh"
symbols = "!@#$%&*"
numbers = "123456789"

a = int(input("Letters: "))
b = int(input("Symbols: "))
c = int(input("Numbers: "))

password = (
    random.choices(letters, k=a)
    + random.choices(symbols, k=b)
    + random.choices(numbers, k=c)
)

random.shuffle(password)

print("".join(password))