import finesse
import operator
import numpy as np
from functools import reduce
from itertools import permutations
from finesse.symbols import expand, collect, coefficient_and_term, Constant, expand_pow


def test_multiply_reordering():
    """Ensure multiplying 2,a,b in any order gives the same final result ordering."""
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    args = [2, a, b]
    for comb in permutations(args):
        assert reduce(operator.mul, comb) == 2 * a * b


def test_multiply_collect():
    a = finesse.symbols.Variable("a")
    args = [2, a, 4]
    for comb in permutations(args):
        assert reduce(operator.mul, comb) == 8 * a


def test_sum():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert str(a + b) == "(a+b)"


def test_sub():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert str(a - b) == "(a-b)"


def test_mul():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert str(a * b) == "a*b"
    assert str(2 * a * b) == "2*a*b"


def test_numpy_fn():
    a = finesse.symbols.Variable("a")
    assert str(np.cos(a)) == "cos(a)"


def test_equality_sum():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    args = [2, a, b]
    for comb in permutations(args):
        assert np.sum(args) == 2 + a + b


def test_equality_mul():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    args = [2, a, b]
    for comb in permutations(args):
        assert np.prod(args) == 2 * a * b


def test_simplify():
    a = finesse.symbols.Variable("a")
    assert (
        3 / a - 2 * (4 * 1 / a - (-5 * 1 / a + 1.0))
    ).expand().collect() == 2 - 15 / a


def test_collect():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert collect(a * a) == a ** 2
    assert collect(a * a ** -1) == 1
    assert collect(a - a) == 0
    assert collect(2 / a - 2 / a) == 0
    assert collect(-2 / a - 3 / a) == -5 / a
    assert collect(2 * 2 / a) == 4 / a
    assert collect(2 * (2 / a)) == 4 / a
    assert collect((1 + 2 / b) + (1 - 2 / b)) == 2
    assert collect(2 * a - a) == a
    assert collect(4 * a - 4 * a) == 0
    assert collect(-2 * a + a) == -a
    assert collect(a + a + 4) == 4 + 2 * a
    assert collect(a + 2 * a) == 3 * a
    assert collect(1.5 * a + 1.5 * a) == 3 * a
    assert collect(np.cos(a) + np.cos(a)) == 2 * np.cos(a)


def test_expand():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert -2 * a * b == -2 * a * b
    assert 2 * a * b == -2 * a * -b
    assert 2 * a * b == 2 * a * b
    assert a * 2 * b == 2 * a * b
    assert a * b * 2 == 2 * a * b
    assert expand(2 * a * (1 + b)) == 2 * a + 2 * a * b
    assert expand(2 * np.cos(a + b)) == 2 * np.cos(a + b)
    assert expand(10 * np.cos(a) * (a + b)) == 10 * np.cos(a) * a + 10 * np.cos(a) * b
    assert expand(3 * (1 + a) ** 2 * (2 + a) ** 2).collect() == (
        12 + 36 * a + 39 * (a) ** (2) + 18 * (a) ** (3) + 3 * (a) ** (4)
    )
    assert expand(2 / a - 6 / (3 * a)).collect() == 0


def test_coefficient_and_term():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert coefficient_and_term(a) == (1, a)
    assert coefficient_and_term(2 * a) == (2, a)
    assert coefficient_and_term(a * b) == (1, a * b)
    assert coefficient_and_term(a + b) == (1, a + b)
    assert coefficient_and_term(Constant(3.3)) == (3.3, None)
    assert coefficient_and_term(np.cos(a)) == (1, np.cos(a))
    assert coefficient_and_term(3.3 * np.cos(a)) == (3.3, np.cos(a))


def test_expand_pow():
    a = finesse.symbols.Variable("a")
    assert expand_pow((2 * a) ** 2) == 4 * a ** 2
    assert expand_pow(1 + (2 * a) ** 2 + 2 * (4 * a) ** 2).collect() == 1 + 36 * a ** 2


def test_matrix_prods():
    from finesse.symbols import Matrix, Variable
    A = Matrix('A')
    B = Matrix('B')
    a = Variable('a') 
    assert((a*B*A*2).args == [2,a,B,A])
    assert((a*B*A*2 - 2*a*B*A).collect() == 0)