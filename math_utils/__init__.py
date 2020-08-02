import pkgutil
maya_loader = pkgutil.find_loader('maya')
if maya_loader:
    from .mVector_math import Vector
else:
    from .vector_math import Vector
__all__ = ['Vector']