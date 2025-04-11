nor = 5  # nor means number of rows

#Top pyramid
for i in range(1, nor + 1):
    print(" " * (nor - i) + "*" * (2 * i - 1))

#Bottom pyramid
for i in range(1, nor):
    print(" " * i + "*" * (2 * (nor - i) - 1))
