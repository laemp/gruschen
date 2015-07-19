import numpy as np


# dynamic time warping - squared
def get_metric(s, t):
    return _get_dtw_matrix(s, t)[-1, -1]


def _get_dtw_matrix(s, t):
    n = len(s)
    m = len(t)
    dtw = _prepare_dtw_matrix(n, m)
    for i in range(1, n+1):
        row = dtw[i, :]
        cost = _cost_vector_euclidean(s[i-1] - t, m)
        row[1:] = _row_prediction(cost, dtw[i-1, :])
        _row_adjustment(row, cost, m)
    return dtw


def _prepare_dtw_matrix(n, m):
    dtw = np.zeros((n+1, m+1))
    dtw[1:, 0] = float("inf")
    dtw[0, 1:] = float("inf")
    dtw[0, 0] = 0
    return dtw


def _cost_vector_euclidean(diff, m):
    return np.fromiter((np.inner(d, d) for d in diff), np.float, m)


# alternative to euclidean distance, test later
def _cost_vector_absolute(diff, m):
    return np.fromiter((np.linalg.norm(d, 1) for d in diff), np.float, m)


def _row_prediction(cost, prev_row):
    return cost + np.minimum(prev_row[0:-1], prev_row[1:])


def _row_adjustment(row, cost, m):
    for j in range(1, m+1):
        if row[j-1] + cost[j-1] < row[j]:   # is true 1 out of 5 times
            row[j] = row[j-1] + cost[j-1]
