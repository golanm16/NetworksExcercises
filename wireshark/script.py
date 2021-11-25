while(True):
    mystr = input("enter string: ")
    if mystr=='':
        break
    sum = 0
    for c in mystr:
        print(f'char {c} value:{ord(c)}')
        sum+=ord(c)

    print(f'sum is {sum}')

