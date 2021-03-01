numbers = [i for i in range(1, 11)]

def make_less_than_filter(max):
    def filter(item):
        return item < max
    return filter

def allMatch(ls, fn):
    for item in ls:
        if not fn(item):
            return False
    return True

print("All numbers are less than 5?", allMatch(numbers, make_less_than_filter(5))) 
print("All numbers are less than 11?", allMatch(numbers, make_less_than_filter(11))) 