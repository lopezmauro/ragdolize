from maya.api import OpenMaya as om

class Vector(object):
    def __init__(self, *args):
        if len(args)==0:
            self.array = om.MVector([0,0,0])
        if len(args)==1:
            self.array = om.MVector(*args)
        else:
            self.array = om.MVector(args)

    def magnitude(self):
        return  self.array.length()

    def normalize(self):
        return Vector(self.array.normal())
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array * other)
        return Vector(self.array * other.array)

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array / other)
        return Vector(self.array / other.array)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array/other)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array + other)
        return Vector(self.array + other.array)
        
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array - other)
        return Vector(self.array - other.array)

    def __iter__(self):
        return iter(self.array)
    
    def __len__(self):
        return 3
    
    def __getitem__(self, key):
        return self.array[key]
    
    def __setitem__(self, key, value):
        self.array[key] = float(value)

    def __repr__(self):
        return str(self.array)

    def __neg__(self):
        return Vector(self.array * -1)


