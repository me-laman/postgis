def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-2) + fib(n-1)


if __name__ == '__main__':
    print(fib(12))




# 1 1 2 3 5 8