"""Do whatever isotonic regression is."""

import numpy as np


def fit(a: np.ndarray) -> np.ndarray:
    n = len(a)
    w = np.ones(n, dtype=np.float64)
    return _fit_with_weights(a, w)


def _fit_with_weights(a: np.ndarray, w: np.ndarray) -> np.ndarray:
    n = len(a)
    assert len(w) == n

    aprime = np.zeros(n, dtype=np.float64)
    wprime = np.zeros(n, dtype=np.float64)
    S = np.zeros(n + 1, dtype=int)

    aprime[0], wprime[0] = a[0], w[0]
    S[0], S[1] = 0, 1
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

        S[j + 1] = i + 1

    y = np.zeros(n, dtype=np.float64)
    for k in range(j + 1):
        for L in range(S[k], S[k + 1]):
            y[L] = aprime[k]

    return y
