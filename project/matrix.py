from typing import List


class Matrix:
    """
    Класс для работы с матрицами, включая сложение, умножение и транспонирование.
    """

    def __init__(self, data: List[List[float]]):
        """
        Инициализирует матрицу.

        :param data: Двумерный список чисел, представляющий матрицу.
        """
        self.data: List[List[float]] = data
        self.rows: int = len(data)
        self.cols: int = len(data[0]) if data else 0

    def __str__(self) -> str:
        """
        Возвращает строковое представление матрицы.

        :return: Строка, представляющая матрицу.
        """
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def add(self, other: "Matrix") -> "Matrix":
        """
        Складывает две матрицы.

        :param other: Вторая матрица для сложения.
        :return: Новая матрица, представляющая сумму.
        :raises ValueError: Если матрицы имеют разные размеры.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def multiply(self, other: "Matrix") -> "Matrix":
        """
        Умножает две матрицы.

        :param other: Вторая матрица для умножения.
        :return: Новая матрица, представляющая произведение.
        :raises ValueError: Если число столбцов первой матрицы не равно числу строк второй матрицы.
        """
        if self.cols != other.rows:
            raise ValueError(
                "Number of columns in the first matrix must equal the number of rows in the second matrix.")

        result = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.cols)) for j in range(other.cols)] for i
                  in range(self.rows)]
        return Matrix(result)

    def transpose(self) -> "Matrix":
        """
        Транспонирует матрицу, меняя строки и столбцы местами.

        :return: Новая транспонированная матрица.
        """
        result = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(result)
