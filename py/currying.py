def add(a, b):
    return a + b

print("Add:", add(5, 5))

def curry_add(a):
    return lambda x: a + x

print("Curry Add:", curry_add(5)(5))