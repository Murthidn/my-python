print('Enter a number!')
try:
    n1=int(input())
    n2=int(input())
    print(int(n1/n2))
    print(n1/n2)
except ValueError:
    print('Not a valid number')