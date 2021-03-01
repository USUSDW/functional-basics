numbers = [i for i in range(1, 11)]

def make_less_than_filter(max):
    def filter(item):
        print(max)
        return item < max
    return filter

def allMatch(ls, fn):
    for item in ls:
        if not fn(item):
            return False
    return True

filter5 = make_less_than_filter(5)
filter11 = make_less_than_filter(11)
print("All numbers are less than 5?", allMatch(numbers, filter5))
print("All numbers are less than 11?", allMatch(numbers, filter11))