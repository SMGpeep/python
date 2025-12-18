x  = 10
y  = 10

print(x is y == x == y)

#case where x == y is True, but x is y is False

x = int('1000')
y = int('1000')

print(x)
print(y)
print(f"x==y: {x == y}")  # True
print(f"x is y: {x is y}")  # False

# Previously, the comment said "case where x == y is False, but x is y is True"
# This is not possible for immutable integers in Python—if x is y, then x == y must always be True.
# The original code used large integers, but Python only interns small integers (-5..256),
# so for 1000, x is y is usually False, and x == y is True.
# There is no case for immutable ints in which x == y is False but x is y is True!

x = 1000
y = 2000

print(x == y)  # False, because 1000 != 2000
print(x is y)  # False, different objects with different values anyway

