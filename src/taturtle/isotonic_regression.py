"""Do whatever isotonic regression is."""

import numpy as np


def fit(
    a: np.ndarray[tuple[int, ...], np.dtype[np.float64]],
) -> np.ndarray[tuple[int], np.dtype[np.float64]]:
    """Fit isotonic regression."""
    n = len(a)
    w = np.ones(n, dtype=np.float64)
    return _fit_with_weights(a, w)


def _fit_with_weights(
    a: np.ndarray[tuple[int, ...], np.dtype[np.float64]],
    w: np.ndarray[tuple[int], np.dtype[np.float64]],
) -> np.ndarray[tuple[int], np.dtype[np.float64]]:
    n = len(a)
    assert len(w) == n

    aprime = np.zeros(n, dtype=np.float64)
    wprime = np.zeros(n, dtype=np.float64)
    weights = np.zeros(n + 1, dtype=int)

    aprime[0], wprime[0] = a[0], w[0]
    weights[0], weights[1] = 0, 1
    j = 0

    for i in range(1, n):
        j += 1
        aprime[j] = a[i]
        wprime[j] = w[i]

        while j > 0 and aprime[j] < aprime[j - 1]:
            aprime[j - 1] = (wprime[j] * aprime[j] + wprime[j - 1] * aprime[j - 1]) / (
                wprime[j] + wprime[j - 1]
            )
            wprime[j - 1] += wprime[j]
            j -= 1

        weights[j + 1] = i + 1

    y = np.zeros(n, dtype=np.float64)
    for k in range(j + 1):
        for weight in range(weights[k], weights[k + 1]):
            y[weight] = aprime[k]

    return y
