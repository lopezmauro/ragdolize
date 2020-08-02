import math
import numbers

class Vector(object):
    def __init__(self, *args):
        if len(args)==0:
            self.array = (0.0, 0.0, 0.0)
        elif len(args)==1:
            self.array = args[0]
        else :
            self.array = args
        
    def magnitude(self):
        return math.sqrt(sum( comp**2 for comp in self.array))

    def normalize(self):
        mag = self.magnitude()
        return Vector(*[comp/mag for comp in self.array])
    
    def inner(self, other):
        return sum(a * b for a, b in zip(self.array, other.array))
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.inner(other)
        elif isinstance(other, numbers.Number):
            return Vector([a * other for a in self.array])

    def __div__(self, other):
        if isinstance(other, numbers.Number):
            return Vector([a / other for a in self.array])

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return Vector([a / other for a in self.array])

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.array, other.array)])
        
    
    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.array, other.array)])

    def __iter__(self):
        return iter(self.array)
    
    def __len__(self):
        return len(self.array)
    
    def __getitem__(self, key):
        return self.array[key]
    
    def __setitem__(self, key, value):
        self.array[key] = float(value)

    def __repr__(self):
        return str([a for a in self.array])

    def __neg__(self):
        return Vector([a*-1 for a in self.array])