import math
from typing import List


class Vector:
    """
    Класс для работы с векторами в многомерном пространстве.
    """

    def __init__(self, components: List[float]):
        """
        Инициализирует вектор с заданными компонентами.

        :param components: Список чисел, представляющих компоненты вектора.
        """
        self.components: List[float] = components

    def __str__(self) -> str:
        """
        Возвращает строковое представление вектора.

        :return: Строка, представляющая вектор.
        """
        return f"Vector({self.components})"

    def length(self) -> float:
        """
        Вычисляет длину (модуль) вектора.

        :return: Длина вектора.
        """
        return math.sqrt(sum(x**2 for x in self.components))

    def dot_product(self, other: "Vector") -> float:
        """
        Вычисляет скалярное произведение с другим вектором.

        :param other: Второй вектор.
        :return: Скалярное произведение векторов.
        :raises ValueError: Если векторы имеют разные размеры.
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for dot product")
        return sum(x * y for x, y in zip(self.components, other.components))

    def angle_between(self, other: "Vector") -> float:
        """
        Вычисляет угол между двумя векторами в радианах.

        :param other: Второй вектор.
        :return: Угол в радианах.
        :raises ValueError: Если хотя бы один из векторов имеет нулевую длину.
        """
        dot_prod = self.dot_product(other)
        length_self = self.length()
        length_other = other.length()

        if length_self == 0 or length_other == 0:
            raise ValueError("Cannot compute angle with zero-length vector")

        cos_theta = dot_prod / (length_self * length_other)
        # Ограничиваем значение cos_theta из-за возможных ошибок округления
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)
