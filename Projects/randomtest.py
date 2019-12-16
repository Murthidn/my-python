import random

r=random.randint(0, 20)
print(r)

print('Enter a num')
n=int(input())

if n==r:
    print('Congrats!!!')
elif n<r:
    print('too low')
else:
    print('too high')