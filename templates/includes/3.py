def func1(x):
    return x * x * x - 3 * x * x + 4 * x - 5


def func2(x):
    return 4 * x * x * x - 6 * x + 10


def func3(x):
    return x * x * x * x - 2 * x * x + 9 * x - 12


# problem 3(a)
print("3(a)")
print("x = 4, f(x) = ", func1(4))
print("x = 8, f(x) = ", func1(8))
print("x = 25, f(x) = ", func1(25))

# problem 3(b)
print("3(b)")

print("x = 4, f(x) = ", func2(4))
print("x = 8, f(x) = ", func2(8))
print("x = 25, f(x) = ", func2(25))

# problem 3(c)
print("3(c)")
print("x = 4, f(x) = ", func3(4))
print("x = 8, f(x) = ", func3(8))
print("x = 25, f(x) = ", func3(25))
