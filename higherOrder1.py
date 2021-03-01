import math

def doFunction(fn):
    return fn()

def printHello():
    print("Hello!")

doFunction(printHello) # Note that we don't have parenthesis on the inside.



def applyToNumber(number, fn):
    return fn(number)

def plus3(number):
    return number + 3

print("Applying plus3:", applyToNumber(4, plus3))



square = lambda number: number * number

# The above square is the same as writing a function like this:
def square2(number):
    return number * number

print("Applying square:", applyToNumber(4, square))

print("Applying math.sqrt:", applyToNumber(4, math.sqrt))

print("Applying anonymous lambda:", applyToNumber(4, lambda x: x * math.pi))