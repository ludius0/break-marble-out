# libs
from typing import Tuple, TypeVar, Union, NamedTuple
import math
import operator
import numbers

__all__ = ["Vec2"]

Variation = Union["Vec2" or Tuple[float, float] or float]

class Vec2(NamedTuple):
    """
    Vector class behaving like tuple, which hold x and y value (can be only floats).
    Mathematical operations:
    >>> Vec2(6, 7) * 2 + Vec2(2., 2.)
    >>> Vec2(14, 16)
    Set/get item:
    >>> v = Vec2(3.2, 1.3)
    >>> v.x # or [0] or ['x']
    >>> 3.2
    >>> v.y = 1
    >>> Vec2(3.2, 1.)
    For every operations or function it returns new Vec2 (better for debugging).
    """
    x: float = 0.
    y: float = 0.

    def __repr__(self) -> str:
        return f"Vec2({self.x:.5f}, {self.y:.5f})"
    
    def __len__(self) -> int: 
        return 2
    
    def __getitem__(self, key: Union[str or int]) -> float:
        assert isinstance(key, (str, int))
        if key == "x" or key == 0: return self.x
        elif key == "y" or key == 1: return self.y
        raise IndexError(f"Invalid key. Should be 0 or 1 or 'x' or 'y'. Got {key}")

    def __add__(self, other: Variation) -> "Vec2":
        if isinstance(other, (float, int)):  
            return Vec2(self.x + other, self.y + other)
        elif isinstance(other, tuple):                          
            return Vec2(self.x + other[0], self.y + other[1])
        raise TypeError
    
    def __radd__(self, other: Variation) -> "Vec2":
        return self.__add__(other)

    def __sub__(self, other: Variation) -> "Vec2":
        if isinstance(other, (float, int)):  
            return Vec2(self.x - other, self.y - other)
        elif isinstance(other, tuple):                          
            return Vec2(self.x - other[0], self.y - other[1])
        raise TypeError

    def __rsub__(self, other: Variation) -> "Vec2":
        return self.__sub__(other)

    def __mul__(self, other: Variation) -> "Vec2":
        if isinstance(other, tuple):
            return Vec2(self.x * other[0], self.y * other[1])
        elif isinstance(other, numbers.Real):
            return Vec2(self.x * other, self.y * other)
        raise TypeError

    def __rmul__(self, other: Variation) -> "Vec2":
        return self.__mul__(other)

    def __floordiv__(self, number: float) -> "Vec2":
        assert isinstance(number, numbers.Real)
        return Vec2(self.x // number, self.y // number)

    def __truediv__(self, number: float) -> "Vec2":
        assert isinstance(number, numbers.Real)
        return Vec2(self.x // number, self.y // number)
    
    def __pow__(self, number: float) -> "Vec2":
        assert isinstance(number, numbers.Real)
        return Vec2(self.x ** number, self.y ** number)

    def __matmul__(self, vector2d: "Vec2") -> "Vec2":
        assert isinstance(vector2d, type(self))
        return float(self.x * vector2d[0] + self.y * vector2d[1])

    def __neg__(self) -> "Vec2":
        return Vec2(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self) -> "Vec2":
        return Vec2(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self) -> float:
        return self.lenght
    
    def __bool__(self) -> bool:
        return self != (0, 0)
    
    def neg(self) -> "Vec2":
        return self.__neg__()
    
    def neg_x(self) -> "Vec2":
        return Vec2(operator.neg(self.x), self.y)

    def neg_y(self) -> "Vec2":
        return Vec2(self.x, operator.neg(self.y))
    
    def pos(self) -> "Vec2":
        return self.__pos__()
    
    def dot(self, vector2d: "Vec2") -> float:
        return self.__matmul__(vector2d)
    
    @property
    def totuple(self) -> tuple:
        return (self.x, self.y)

    @property
    def normalization(self) -> "Vec2":
        return self * (1 / self.lenght)
    
    @property
    def lenght(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2) # math.hypot()
    
    @property
    def length_sqrd(self) -> float:
        return self.x ** 2 + self.y ** 2
    
    def distance_to(self, vector2d) -> float:
        assert isinstance(vector2d, type(self))
        return math.sqrt((self.x - vector2d.x) ** 2 + (self.y - vector2d.y) ** 2)
    
    def cross(self, other: Variation) -> "Vec2":
        return self.x * other[1] - self.y * other[0]
    
    def cos_theta(self, vector2d: "Vec2") -> float:
        assert isinstance(vector2d, type(self))
        return self * vector2d / (self.lenght * vector2d.lenght)

    def rotated(self, angle_radians: float) -> "Vec2":
        assert isinstance(angle_radians, numbers.Real)
        sin_n, cos_n = math.sin(angle_radians), math.cos(angle_radians) 
        return Vec2(self.x * cos_n - self.y * sin_n, \
            self.x * sin_n + self.y * cos_n)

    def rotated_degrees(self, angle_of_degrees: float) -> "Vec2":
        assert isinstance(angle_of_degrees, numbers.Real)
        return self.rotated(math.radians(angle_of_degrees))
    
    def get_angle(self) -> float:
        return 0. if self.length_sqrd == 0. else math.degrees(math.atan2(self.y, self.x))

    def get_angle_between(self, vector2d: "Vec2") -> float:
        return math.degrees(math.atan2(self.cross(vector2d), self.dot(vector2d)))

    def perpendicular(self) -> "Vec2":
        return Vec2(-self.y, self.x)

    def perpendicular_normal(self) -> "Vec2":
        if self.length != 0: 
            return Vec2(-self.y / self.length, self.x / self.length)
        return self

    def interpolate_to(self, other: "Vec2", range_: float) -> "Vec2":
        return Vec2(self.x + (other[0] - self.x) * range_, \
            self.y + (other[1] - self.y) * range_)

    def convert_to_basis(self, x_vec: "Vec2", y_vec: "Vec2") -> "Vec2":
        return Vec2(self.dot(x_vec) / x_vec.length_sqrd, \
            self.dot(y_vec) / y_vec.length_sqrd)
    
    def copy(self) -> "Vec2":
        return self
    
    @staticmethod
    def zeros() -> "Vec2":
        return Vec2(0, 0)

    @staticmethod
    def ones() -> "Vec2D":
        return Vec2(1, 1)

    @staticmethod
    def unit() -> "Vec2D":
        return Vec2(0, 1)