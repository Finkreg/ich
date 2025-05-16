import pytest
from simple_math import SimpleMath

@pytest.fixture
def simple_math_instance():
    return SimpleMath()

def test_square_positive_number(simple_math_instance):
    assert simple_math_instance.square(2) == 4

def test_square_negative_number(simple_math_instance):
    assert simple_math_instance.square(-3) == 9

def test_square_zero(simple_math_instance):
    assert simple_math_instance.square(0) == 0

def test_cube_positive_number(simple_math_instance):
    assert simple_math_instance.cube(3) == 27

def test_cube_negative_number(simple_math_instance):
    assert simple_math_instance.cube(-3) == -27

def test_cube_zero(simple_math_instance):
    assert simple_math_instance.cube(0) == 0