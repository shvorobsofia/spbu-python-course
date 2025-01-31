import pytest
import math
from project.vectors import Vector
def test_vector_length():
    v = Vector([3, 4])
    assert v.length() == 5

def test_dot_product():
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, -5, 6])
    assert v1.dot_product(v2) == 12

def test_angle_between():
    v1 = Vector([1, 0])
    v2 = Vector([0, 1])
    assert math.isclose(v1.angle_between(v2), math.pi / 2, rel_tol=1e-6)

def test_dot_product_dimension_mismatch():
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5])
    with pytest.raises(ValueError, match="Vectors must have the same dimension for dot product"):
        v1.dot_product(v2)

def test_angle_with_zero_length_vector():
    v1 = Vector([0, 0, 0])
    v2 = Vector([1, 2, 3])
    with pytest.raises(ValueError, match="Cannot compute angle with zero-length vector"):
        v1.angle_between(v2)
