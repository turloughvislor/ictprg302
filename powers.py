#!/usr/bin/python3

def square(num):
    return num * num

def cube(num):
    return num * num * num
    


def main():
    print('reverse the polarity of the neutron flow')
    n = int(input('Enter a number: '))
    seq = 1
    while seq <= n:
        squ = square(seq)
        cub = cube(seq)
        print(f'The number is {seq}, its square is {squ} and its cube is {cub}.')
        seq += 1

if __name__ == '__main__':
    main()