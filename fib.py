def fib(num):
    if num<2:
        return 1
    return fib(num-1) +fib(num-2)

def fib2(num):
    if num<2:
        return 1
    x1,x2 = 1,1
    for i in range(num-1):
        tmp = x2
        x2+=x1
        x1 = tmp
    return x2