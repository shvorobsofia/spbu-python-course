import pytest
from project.matrix import Matrix


def test_matrix_addition():
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])
    expected = Matrix([[6, 8], [10, 12]])
    assert A.add(B).data == expected.data


def test_matrix_addition_dimension_mismatch():
    A = Matrix([[1, 2, 3], [4, 5, 6]])
    B = Matrix([[7, 8], [9, 10]])
    with pytest.raises(
        ValueError, match="Matrices must have the same dimensions for addition."
    ):
        A.add(B)


def test_matrix_multiplication():
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[2, 0], [1, 2]])
    expected = Matrix([[4, 4], [10, 8]])
    assert A.multiply(B).data == expected.data


def test_matrix_multiplication_dimension_mismatch():
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6, 7]])
    with pytest.raises(
        ValueError,
        match="Number of columns in the first matrix must equal the number of rows in the second matrix.",
    ):
        A.multiply(B)


def test_matrix_transpose():
    A = Matrix([[1, 2, 3], [4, 5, 6]])
    expected = Matrix([[1, 4], [2, 5], [3, 6]])
    assert A.transpose().data == expected.data
