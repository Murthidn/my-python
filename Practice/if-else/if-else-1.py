try:
    print('Enter a number!')
    n=int(input())
    if n%2==0:
        if n in range(2, 5):
            print('Not weird!')
        elif n in range(6, 20):
            print('Weird!')
        elif n > 20:
            print('Not weird!')
        else:
            print('Not in condition!')
    else:
        print('Weird')

except ValueError:
    print('Not a valid number, please enter integer format!')



