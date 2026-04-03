a = 'picscip'
palindrome = True
count = 0
for i in range(0,len(a)//2):
    if a[i]==a[len(a)-i-1]:
        count+=1
    else:
        palindrome = False
if count == len(a)//2:
    palindrome = True
print(palindrome)
