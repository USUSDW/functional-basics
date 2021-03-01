def get_points(axis_len=5, centerX = 0, centerY = 0):
    """
    Builds a list of discrete points that has axis_len units across its
    diagonal, centered at centerX, centerY.
    """
    return [((x//axis_len) + centerX - axis_len // 2, 
        (x%axis_len) + centerY - axis_len // 2) 
        for x in range (axis_len ** 2)]

points = get_points(5)

f = lambda x, y: x * 10 - y * 5
g = lambda x, y: x + y
h = lambda x, y: x ** 2

max_f = max(points, key=lambda x: f(x[0], x[1]))
max_g = max(points, key=lambda x: g(x[0], x[1]))
max_h = max(points, key=lambda x: h(x[0], x[1]))

print("Max f(x, y):", max_f)
print("Max g(x, y):", max_g)
print("Max h(x, y):", max_h)