# Introduction to Functional Programming

*By [Hunter Henrichsen](https://github.com/hhenrichsen)*
*and [Makayden Lofthouse](https://github.com/mloft74)*

Functional programming isn't some amazing silver-bullet tool that can solve
every problem that you have. That said, it's changed a lot of how I think
about code, and has made some problems that used to be vastly complex into
problems that are much more simple and elegant to solve.

## Introduction
The functional programming paradigm introduces a couple of ideas that make it
straightforward. Adopting these practices can lead to much better code. Today
we're going to go through five different practices today:
* Immutability
* Pure Functions
* Higher-Order Functions
* Currying
* Closure

One of the biggest parts of functional programming is treating functions just
like any other type. That means they can be stored in variables, can be
manipulated, and can be passed around to other functions. Before we get as
crazy as functions taking functions as parameters, let's talk about some of
the basics.

## Immutability
Immutability is not quite functional on its own, but is very close to
functional programming. At its core, it's the idea that data should only be
able to be changed by creating a new version of it.

Let's take a look in python:

[`immutability.py`](py/immutability.py)
```python
# Useful typing things.
from __future__ import annotations
from numbers import Number

class Fraction():
    def __init__(self, numerator: Number, denominator: Number):
        self.__NUMERATOR = numerator
        self.__DENOMINATOR = denominator

    def get_numerator(self) -> Number:
        return self.__NUMERATOR

    def get_denominator(self) -> Number:
        return self.__DENOMINATOR

    def __str__(self) -> str:
        return f"{self.__NUMERATOR}/{self.__DENOMINATOR}"

    def __repr__(self) -> str:
        return f"{self.__NUMERATOR}/{self.__DENOMINATOR}"

    def __rmul__(self, other: Fraction):
        return self.__mul__(other)

    def __mul__(self, other: Fraction):
        assert isinstance(other, Fraction)
        return Fraction(
            self.get_numerator() * other.get_numerator(),
            self.get_denominator() * other.get_denominator())

    def get_value(self) -> Number:
        return self.get_numerator() / self.get_denominator()

    def copy(self, **kwargs):
        """
        Returns a copy of this fraction with values changed if provided.
        Accepts two keyword args, numerator and denominator. Copies the
        values from self otherwise.
        """
        numerator = self.__NUMERATOR
        if "numerator" in kwargs:
            assert isinstance(kwargs["numerator"], Number)
            numerator = kwargs["numerator"]

        denominator = self.__DENOMINATOR
        if "denominator" in kwargs:
            assert isinstance(kwargs["denominator"], Number)
            denominator = kwargs["denominator"]

        return Fraction(numerator, denominator)

# Let's make a fraction
fraction1 = Fraction(1, 2)
print("Fraction 1:", fraction1)
print("Fraction 1's Value:", fraction1.get_value())
# Not allowed:
fraction1.__NUMERATOR = 5
print("Fraction 1:", fraction1)
# Let's make a new copy instead
fraction2 = fraction1.copy(numerator=5)
print("Fraction 2:", fraction2)
# Fraction 1 is untouched.
print("Fraction 1:", fraction1)
# We can multiply them as well.
print("Fraction 1 x Fraction 2:", fraction1 * fraction2)
# Fraction 1 is still untouched.
print("Fraction 1:", fraction1)
```

This outputs:
```
Fraction 1: 1/2
Fraction 1's Value: 0.5
Fraction 1: 1/2
Fraction 2: 5/2
Fraction 1: 1/2
Fraction 1 x Fraction 2: 5/4
Fraction 1: 1/2
```

Notice how no matter how hard we try, the only way to change a value of one of
the parts of this class is by making a copy with `.copy()`, or by making a new
instance of the class. This can just as easily be recreated in Java, C#, and
JavaScript (although that one requires another concept we'll talk about later).

### Benefits
So what do we gain from this? The first thing is a reduction in bugs. Many bugs
that I have found arise from something changing something that it should not be
changing, or should not have access to change.

Another benefit is the fact that we know that operations we do on this data
will not harm the internals of this class, and can safely do operations.

### Drawbacks
There are a couple drawbacks, though. Even this python example is a lot more
complex (especially the `.copy()` function) than a mutable class would be. In
addition, these take up more memory because every time you want a new fraction
or do a new operation on the fraction, you have to make a new class.

It's up to you to decide whether the benefits outweigh the drawbacks, but
either way they lead us to the next idea: Pure Functions.

## Pure Functions
Pure Functions are functions that treat their data as if it were immutable, or
in other words, they have no side effects. Anything passed to the function
leaves the function in the same state that it went in. Having immutable data
makes writing pure functions trivially easy, but unfortunately not everything
is immutable by default.

Let's take a look using python lists:

[`pure.py`](py/pure.py)
```python
def addNextImpure(ls: list):
    top = ls[-1]
    # Side effect right here!
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
```

Outputs:
```
Using a non-pure function:
Numbers 1: [1, 2, 3, 4, 5]
Numbers 1: [1, 2, 3, 4, 5, 6]
Using a pure function:
Numbers 2: [1, 2, 3, 4, 5]
Numbers 2: [1, 2, 3, 4, 5]
Numbers 3: [1, 2, 3, 4, 5, 6]
```

Notice how after we run the impure function on Numbers 1, we end up with an
extra item in there. While this is something we learn happens early on in
Python, it's not entirely expected because of the way that other types of
variables work.

Immutability and pure functions go hand in hand. Writing one makes writing
the other easy. If all we write are pure functions, it doesn't matter if data
is mutable or not because we always treat it like it's immutable.

### Benefits
Code written like this is really good in code that other people will use,
because it means what they put in and get out are exactly what they expect,
and they don't need to develop super deep knowledge of your code in order to
use it.

### Drawbacks
Like with Immutability, this type of code can be trickier to write because
you have to be aware of data coming in and make sure that you're not
accidentally changing it. In addition, this can also suffer from increased
memory use because you have to create and maintain copies of what comes in if
they are already not immutable.

## Higher-Order Functions
The two ideas we've talked about before tend to be interesting, but not
particularly ground-shaking or mind-blowing. This is where things changed for
me, at least.

### Higher-Order Basics
Higher-order functions are functions that take a function as a parameter, or
functions that return a function. That's the whole idea, but understanding
why that's useful takes some time.

Let's first learn how to take and pass functions as parameters, then use them
inside of functions:

[`higherOrder1.py`](py/higherOrder1.py#L1-L9)
```python
import math

def doFunction(fn):
    return fn()

def printHello():
    print("Hello!")

doFunction(printHello) # Note that we don't have parenthesis on the inside.
```
Output:
```
Hello!
```

That looks pretty simple, right? We just pass a function in without
parenthesis, then add the parenthesis later. Let's try that with some other
types of parameters.

[`higherOrder1.py`](py/higherOrder1.py#L13-L19)
```python
def applyToNumber(number, fn):
    return fn(number)

def plus3(number):
    return number + 3

print("Applying plus3:", applyToNumber(4, plus3))
```
Output:
```
Applying plus3: 7
```

And now let's introduce the lambda, something that makes creating those 
same functions a whole lot easier:

[`higherOrder1.py`](py/higherOrder1.py#L23-L33)
```python
square = lambda number: number * number

# The above square is the same as writing a function like this:
def square2(number):
    return number * number

print("Applying square:", applyToNumber(4, square))

print("Applying math.sqrt:", applyToNumber(4, math.sqrt))

print("Applying anonymous lambda:", applyToNumber(4, lambda x: x * math.pi))
```

Output:
```
Applying square: 16
Applying math.sqrt: 2.0
Applying anonymous lambda: 12.566370614359172
```

### Higher-Order and Lists
Lists and higher-order functions work really well together. Nearly anything
that requires a loop can also be accomplished with a higher-order function.

To start, let's try writing a function that looks through the list and makes
sure every value in the list matches some criteria.

[`higherOrder2.py`](py/higherOrder2.py#L1-L10)
```python
numbers = [i for i in range(1, 11)]

def allMatch(ls, fn):
    for item in ls:
        if not fn(item):
            return False
    return True

print("All numbers are even?", allMatch(numbers, lambda x: x % 2 == 0))
print("All numbers are less than 10?", allMatch(numbers, lambda x: x <= 10))
```
Output:
```
All numbers are even? False
All numbers are less than 10? True
```
The functions we're using here are called **Predicates**, because they take in
some value and tell us whether or not it matches. In other words, any function
that takes in a value and returns a boolean can be called a predicate.

Now let's try manipulating the list. Instead of reducing it all down into one
value, what if we instead ran an operation on every value and kept track of 
what it returned?

This is called a `map` function.

[`higherOrder2.py`](py/higherOrder2.py#L12-L18)
```python
def map(ls, fn):
    results = []
    for item in ls:
        results.append(fn(item))
    return results

print("Applying square to numbers:", map(numbers, lambda x: x * x))
```
Output:
```
Applying square to numbers: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

### Returning Functions
I mentioned before that functions can also return functions. Here's an
example of a modified version of the above where we return another function
from the inside of a function.

[`higherOrder3.py`](py/higherOrder3.py)
```python
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
```
Output:
```
All numbers are less than 5? False
All numbers are less than 11? True
```

### In the Standard Library

Functional Programming is supported in most languages, and that's reflected in
the standard libraries for them. Python is no exception to this. This is one 
example where the built-in `max` function is used to find the points that 
maximize a function.

[`higherOrder4.py`](py/higherOrder4.py)
```python
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
```
Output:
```
Max f(x, y): (2, -2)
Max g(x, y): (2, 2)
Max h(x, y): (-2, -2)
```

There's also a useful built-in `functools` package that adds some other options.

[`higherOrder5.py`](py/higherOrder5.py)
```python
import functools

numbers = [i for i in range(21)]

summed = functools.reduce(lambda x, y: x + y, numbers)
# This is another builtin but I think it's worth including here.
offset = list(map(lambda x: x + 10, numbers))

print("Summed", summed)
print("Offset", offset)
```
Output:
```
Summed 210
Offset [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
```

### Common Higher-Order Functions
There are also common higher-order functions. We've already implemented `map`
(run an operation on every value in a list) and `all` (make sure each value
matches the predicate given) on our own. Here are a list of others that I'm
familiar with:
* `some` - Sees if *any* of the values match a predicate.
* `reduce` - Turns a list into a single value using a binary function.
* `filter` - Gives back a list of things that match a predicate.
* `forEach` - Runs an operation on each item in the list, returning nothing.

## Capture and Closure

Closure is building a function in such a way that it also carries along 
specific data that it needs. Closure has actually popped up in one of the 
examples so far, remember this one:

```python
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
```
Output:
```
All numbers are less than 5? False
All numbers are less than 11? True
```

Notice how the `max` variable keeps its value even after we call the function
again. To make this more explicit, we can run the code like this:

[`closure1.py`](py/closure1.py)
```python
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
print("All numbers are less than 5?", allMatch(numbers, filter5))) 
print("All numbers are less than 11?", allMatch(numbers, filter11))) 
```
Output:
```
5
5
5
5
5
All numbers are less than 5? False
11
11
11
11
11
11
11
11
11
11
All numbers are less than 11? True
```
Notice how even though we're calling the function later, `filter5` still has 
max defined as 5. We also see something cool here, which shows that our 
allMatch function short-circuits properly because we only see 5 prints before
we get to the `False`.

You can use this to your advantage to get data (and other functions!) that are
a part of a function's scope without exposing them to the world, like so:

[`closure2.py`](py/closure2.py)
```python
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
```
Output:
```
Add: 12
Mult: 16
Add after incr: 13
Mult after incr: 20
```

It's super clear here that there's no way for anyone to try to get n2, so the
only ways to modify it is with the functions that we return back. This helps us
build code that has a clear way to use it.

## Currying

Currying is the process of converting a function with multiple arguments into
a multiple function calls of single arguments. 

[`currying.py`](py/currying.py)
```python
def add(a, b):
    return a + b

print("Add:", add(5, 5))

def curry_add(a):
    return lambda x: a + x

print("Curry Add:", curry_add(5)(5))
```
Output:
```
Add: 10
Curry Add: 10
```

## Other Language Demos