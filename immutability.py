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