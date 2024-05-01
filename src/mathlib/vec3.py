import math

class vec3:
    def __init__(self, x=None, y=None, z=None):
        if x == None:
            self.e = [0.0, 0.0, 0.0]
        elif y == None:
            self.e = [x, x, x]
        else:
            self.e = [x, y, z]
    def x(self) -> float:
        return self.e[0]
    def y(self) -> float:
        return self.e[1]
    def z(self) -> float:
        return self.e[2]
    def r(self) -> float:
        return self.e[0]
    def g(self) -> float:
        return self.e[1]
    def b(self) -> float:
        return self.e[2]

    def __str__(self):
        return f'{self.e[0]}, {self.e[1]}, {self.e[2]}'

    def __add__(self, other):
        return vec3(self.e[0] + other.e[0], 
                    self.e[1] + other.e[1],
                    self.e[2] + other.e[2])

    def __sub__(self, other):
        return vec3(self.e[0] - other.e[0], 
                    self.e[1] - other.e[1],
                    self.e[2] - other.e[2])

    def __mul__(self, other):
        if isinstance(other, vec3):
            return vec3(self.e[0] * other.e[0], 
                        self.e[1] * other.e[1],
                        self.e[2] * other.e[2])
        elif isinstance(other, float) or isinstance(other, int):
            return vec3(self.e[0] * other,
                        self.e[1] * other,
                        self.e[2] * other)

    def __radd__(self, other):
        return vec3(self.e[0] + other.e[0], 
                    self.e[1] + other.e[1],
                    self.e[2] + other.e[2])

    def __rsub__(self, other):
        return vec3(self.e[0] - other.e[0], 
                    self.e[1] - other.e[1],
                    self.e[2] - other.e[2])

    def __rmul__(self, other):
        if isinstance(other, vec3):
            return vec3(self.e[0] * other.e[0], 
                        self.e[1] * other.e[1],
                        self.e[2] * other.e[2])
        elif isinstance(other, float) or isinstance(other, int):
            return vec3(self.e[0] * other,
                        self.e[1] * other,
                        self.e[2] * other)

    def __truediv__(self, other):
        if isinstance(other, vec3):
            return vec3(self.e[0] / other.e[0], 
                        self.e[1] / other.e[1],
                        self.e[2] / other.e[2])
        elif isinstance(other, float) or isinstance(other, int):
            return vec3(self.e[0] / other,
                        self.e[1] / other,
                        self.e[2] / other)

    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])

    def __pos__(self):
        return vec3(self.e[0], self.e[1], self.e[2])

    def norm_sqr(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def norm(self):
        return math.sqrt(self.norm_sqr())

    def normalized(self):
        return self / self.norm()

    def safe_normalized(self):
        if self.norm() < 0.0001:
            return vec3(0.0, 0.0, 0.0)
        return self / self.norm()

    @staticmethod
    def zero():
        return vec3(0.0, 0.0, 0.0)

def dot(a:vec3, b:vec3):
    return a.e[0] * b.e[0] + a.e[1] * b.e[1] + a.e[2] * b.e[2]

def cross(a:vec3, b:vec3):
    return vec3(a.e[1] * b.e[2] - a.e[2] * b.e[1],
                a.e[2] * b.e[0] - a.e[0] * b.e[2],
                a.e[0] * b.e[1] - a.e[1] * b.e[0])

