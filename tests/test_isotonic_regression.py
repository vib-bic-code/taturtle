import numpy as np

from taturtle.isotonic_regression import fit


def test_first() -> None:
    data = np.asarray(
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype=np.float64
    )
    expected = np.asarray(
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype=np.float64
    )
    assert np.array_equal(expected, fit(data))


def test_second() -> None:
    data = np.asarray(
        [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0], dtype=np.float64
    )
    expected = np.asarray(
        [5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5], dtype=np.float64
    )
    assert np.array_equal(expected, fit(data))


def test_third() -> None:
    data = np.asarray([1.0, 2.0, 1.8, 1.5, 4.0, 5.0, 4.8, 8.0, 10.0], dtype=np.float64)
    expected = np.asarray(
        [
            1.0,
            1.7666666666666666,
            1.7666666666666666,
            1.7666666666666666,
            4.0,
            4.9,
            4.9,
            8.0,
            10.0,
        ],
        dtype=np.float64,
    )
    assert np.array_equal(expected, fit(data))


def test_fourth() -> None:
    data = np.asarray([1.0, 2.0, 1.8, 1.5, 4.0, 5.0, 4.8, 8.0, 7.0], dtype=np.float64)
    expected = np.asarray(
        [
            1.0,
            1.7666666666666666,
            1.7666666666666666,
            1.7666666666666666,
            4.0,
            4.9,
            4.9,
            7.5,
            7.5,
        ],
        dtype=np.float64,
    )
    assert np.array_equal(expected, fit(data))


def test_fifth() -> None:
    data = np.asarray([1.0], dtype=np.float64)
    expected = np.asarray([1.0], dtype=np.float64)
    assert np.array_equal(expected, fit(data))


def test_sixth() -> None:
    data = np.asarray([2.0, 1.0], dtype=np.float64)
    expected = np.asarray([1.5, 1.5], dtype=np.float64)
    assert np.array_equal(expected, fit(data))
