import numpy as np

import npx


def test_1d():
    a = [1, 2, 1]
    a_unique = npx.unique_rows(a)
    assert np.all(a_unique == [1, 2])


def test_2d():
    a = [[1, 2], [1, 4], [1, 2]]
    a_unique = npx.unique_rows(a)
    assert np.all(a_unique == [[1, 2], [1, 4]])


def test_3d():
    # entries are matrices
    # fails for some reason. keep an eye on
    # <https://stackoverflow.com/q/67128631/353337>
    a = [[[3, 4], [-1, 2]], [[3, 4], [-1, 2]]]
    a_unique = npx.unique_rows(a)
    assert np.all(a_unique == [[[3, 4], [-1, 2]]])


def test_return_all():
    a = [[1, 2], [1, 4], [1, 2]]
    a_unique, inv, count = npx.unique_rows(a, return_inverse=True, return_counts=True)
    assert np.all(a_unique == [[1, 2], [1, 4]])
    assert np.all(inv == [0, 1, 0])
    assert np.all(count == [2, 1])


def test_empty():
    # empty mesh
    a = np.empty((1, 0), dtype=int)
    a_unique = npx.unique_rows(a)
    assert np.all(a_unique == [[]])

    a = np.empty((0, 2), dtype=int)
    a_unique = npx.unique_rows(a)
    assert np.all(a_unique == a)


def test_float():
    a = [1.1, 1.2, 1.1]
    out = npx.unique_rows(a)
    ref = np.array([1.2, 1.1])
    assert np.all(np.abs(out - ref) < 1.0e-14)


def test_float_rows():
    a = [[1.1, 0.7], [1.0, 1.2], [1.1, 0.7]]
    out = npx.unique_rows(a)
    ref = [[1.0, 1.2], [1.1, 0.7]]
    assert np.all(np.abs(out - ref) < 1.0e-14)
