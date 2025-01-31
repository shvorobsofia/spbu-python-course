import math
from typing import List


class Vector:
    def __init__(self, components: List[float]):
        self.components = components

    def __str__(self):
        return f"Vector({self.components})"

    def length(self) -> float:
        return math.sqrt(sum(x ** 2 for x in self.components))

    def dot_product(self, other: 'Vector') -> float:
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for dot product")
        return sum(x * y for x, y in zip(self.components, other.components))

    def angle_between(self, other: 'Vector') -> float:
        dot_prod = self.dot_product(other)
        length_self = self.length()
        length_other = other.length()

        if length_self == 0 or length_other == 0:
            raise ValueError("Cannot compute angle with zero-length vector")

        cos_theta = dot_prod / (length_self * length_other)
        # Ограничиваем значение cos_theta из-за возможных ошибок округления
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)

