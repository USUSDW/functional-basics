def addNextImpure(ls: list):
    top = ls[-1]
    ls.append(top + 1)

def addNextPure(ls: list):
    top = ls[-1]
    newList = ls.copy()
    newList.append(top+1)
    return newList

numbers1 = [1, 2, 3, 4, 5]
numbers2 = [1, 2, 3, 4, 5]

print("Using a non-pure function:")
print("Numbers 1:", numbers1)
addNextImpure(numbers1)
print("Numbers 1:", numbers1)

print("Using a pure function:")
print("Numbers 2:", numbers2)
numbers3 = addNextPure(numbers2)
print("Numbers 2:", numbers2)
print("Numbers 3:", numbers3)
