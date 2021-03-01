numbers = [i for i in range(1, 11)]

def allMatch(ls, fn):
    for item in ls:
        if not fn(item):
            return False
    return True

print("All numbers are even?", allMatch(numbers, lambda x: x % 2 == 0))
print("All numbers are less than 10?", allMatch(numbers, lambda x: x <= 10))

def map(ls, fn):
    results = []
    for item in ls:
        results.append(fn(item))
    return results

print("Applying square to numbers:", map(numbers, lambda x: x * x))