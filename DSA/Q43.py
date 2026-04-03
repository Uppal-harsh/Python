#in a dictionary with key value,pair of starting letter print the string which does not contain any vowel
D = {'a':'apple', 'b':'plwm', 'c':'cherry', 'd': 'lytr'}
vowels = ['a', 'e', 'i', 'o', 'u']

for k,v in D.items():
    vowel = False
    for i in v:
        if i in vowels:
            vowel = True
    if not vowel:
        print(v)

