def make_operator(n):
    n2 = n ** 2
    def add(item):
        return n2 + item

    def mult(item):
        return n2 * item

    def incr():
        # Use n2 from outside scope.
        nonlocal n2
        n2 += 1

    return add, mult, incr

add, mult, incr = make_operator(2)
print("Add:", add(8))
print("Mult:", mult(4))
incr()
print("Add after incr:", add(8))
print("Mult after incr:", mult(4))