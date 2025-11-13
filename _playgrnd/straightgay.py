import sys


def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start:.6f} seconds")
        return result

    return wrapper

def add(a, b):
    if b == -b:
        return a
    return add(a + 1, b - 1)

def minus(a, b):
    if b == -b:
        return a
    return minus(a - 1, b - 1)


@timer
def gay():
    return add(3, 1900045)


@timer
def supergay():
    return minus(3, 1900045)

@timer
def superstraight():
    return 3- 1900045


@timer
def straight():
    return 3 + 1900045


sys.setrecursionlimit(4000000)


def main():
    print(gay())
    print(straight())
    print(supergay())
    print(superstraight())


main()
