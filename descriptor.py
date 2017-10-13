# 有理数计算系统
from math import gcd


def gcdx(x, y):
    x, y = abs(x), abs(y)
    while x > 0:
        x, y = y % x, x
    return y


class Rational:
    def __init__(self, numer, denom):
        if denom == 0:
            raise ValueError("Denom not be zero")
        g = gcd(numer, denom)
        self._numer = numer // g
        self._denom = denom // g

    def __call__(self):
        return Rational

    def __str__(self):
        if self.numer == 0:
            return '0'
        elif self.denom == 1:
            return str(self.numer)
        else:
            return "{}/{}".format(self.numer, self.denom)

    __repr__ = __str__

    @property
    def numer(self):
        return self._numer

    @numer.setter
    def numer(self, v):
        self._numer = v // gcd(v, self._denom)

    @property
    def denom(self):
        return self._denom

    @denom.setter
    def denom(self, v):
        self._denom = v // gcd(self._numer, v)

    # 实现常用方法
    def __add__(self, other):
        numer = self.numer*other.denom + self.denom*other.numer
        denom = self.denom*other.denom
        return Rational(numer, denom)

    def __radd__(self, other):
        return Rational(other * self._denom + self._numer, self._denom)

    def __sub__(self, other):
        numer = self.numer * other.denom - self.denom * other.numer
        denom = self.denom * other.denom
        if numer == 0:
            return 0
        return Rational(numer, denom)

    def __mul__(self, other):
        n2 = getattr(other, 'numer', other)
        d2 = getattr(other, 'denom', 1)
        return Rational(self._numer * n2, self._denom * d2)

    def __truediv__(self, other):
        n2 = getattr(other, 'numer', other)
        d2 = getattr(other, 'denom', 1)
        return Rational(self._numer * d2, self._denom * n2)

    def __neg__(self):
        return Rational(-self._numer, self._denom)

    def __float__(self):
        return self._numer / self._denom

    def __eq__(self, other):
        # ==
        n2 = getattr(other, 'numer', other)
        d2 = getattr(other, 'denom', 1)
        return self._numer==n2 and self._denom==d2

    def __gt__(self, other):
        # >
        n2 = getattr(other, 'numer', other)
        d2 = getattr(other, 'denom', 1)
        return self._numer*d2 > self._denom*n2

    def __lt__(self, other):
        # <
        n2 = getattr(other, 'numer', other)
        d2 = getattr(other, 'denom', 1)
        return self._numer*d2 < self._denom*n2

    def __le__(self, other):
        # <=
        n2 = getattr(other, 'numer', other)
        d2 = getattr(other, 'denom', 1)
        return self._numer*d2 <= self._denom*n2

    def __bool__(self):
        return self._numer != 0


if __name__ == '__main__':
    from random import randrange
    for i in range(100):
        a, b = randrange(100), randrange(100)
        n1 = Rational(a, b)
        n2 = Rational(a, b)
        print(n1 + n2)
        n1 += n2
        print(n1)
        print(n1 > n2)
        print(float(n1))
        print(-n2)





