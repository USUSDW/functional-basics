import functools

numbers = [i for i in range(21)]

summed = functools.reduce(lambda x, y: x + y, numbers)
offset = list(map(lambda x: x + 10, numbers))

print("Summed", summed)
print("Offset", offset)