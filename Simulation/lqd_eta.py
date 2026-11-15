"""
Log Quantile Density (LQD) transformation on an interior quantile grid.

This variant of :mod:`lqd` avoids the quantile endpoints by using an
equally-spaced grid on ``[eta, 1 - eta]``.  The default keeps the original
number of grid points (21) and uses ``eta = 1e-3``.
"""

import numpy as np


def _kde_1d(x, grid, bw):
    """Fast 1D Gaussian KDE evaluated at *grid* points."""
    n = len(x)
    if n < 2 or bw <= 1e-15:
        return np.ones_like(grid) / max(len(grid), 1)
    scaled = (grid[:, None] - x[None, :]) / bw
    kernel = np.exp(-0.5 * scaled ** 2)
    dens = kernel.sum(axis=1) / (n * bw * np.sqrt(2.0 * np.pi))
    return dens


def _estimate_bandwidth(y_slice):
    """R's bw.nrd0: 0.9 * min(sd, IQR/1.34) * n^(-1/5)."""
    sd_val = np.std(y_slice, ddof=1)
    iqr_val = np.percentile(y_slice, 75) - np.percentile(y_slice, 25)
    return 0.9 * min(sd_val, iqr_val / 1.34) * len(y_slice) ** (-0.2)


def LQD(y, idx, t=None, eta=1e-3):
    """
    Log Quantile Density (LQD) transformation.

    When ``t`` is not supplied, use 21 equally-spaced points

    ``t_r = eta + (r - 1) / (21 - 1) * (1 - 2 * eta)``, ``r = 1, ..., 21``.

    Parameters
    ----------
    y : ndarray, shape (n, p)
        Data matrix: *n* samples, *p* variables (flattened image).
    idx : ndarray, shape (m, w*w)
        Index matrix; each row contains 0-based column indices of pixels in
        one sub-region.
    t : ndarray, optional
        Explicit quantile grid.  If supplied, it takes precedence over
        ``eta``.
    eta : float, optional
        Interior-grid boundary.  Must satisfy ``0 < eta < 0.5``.  The
        default is ``1e-3``.

    Returns
    -------
    G : list of ndarray
        Each element has shape ``(n, len(t))``.
    """
    if t is None:
        if not np.isscalar(eta) or not np.isfinite(eta) or not 0 < eta < 0.5:
            raise ValueError("eta must be a finite scalar in (0, 0.5)")
        t = np.linspace(eta, 1.0 - eta, 21)
    else:
        t = np.asarray(t, dtype=float)

    y = np.asarray(y, dtype=float)
    m, n = idx.shape[0], y.shape[0]

    QD = []
    for j in range(m):
        qd = np.zeros((n, len(t)))
        col_idx = idx[j, :].astype(int)
        for i in range(n):
            y_slice = y[i, col_idx]

            bw = _estimate_bandwidth(y_slice)
            grid_min = y_slice.min() - 3.0 * bw
            grid_max = y_slice.max() + 3.0 * bw
            g = np.linspace(grid_min, grid_max, 256)
            dens = _kde_1d(y_slice, g, bw)
            dens[dens <= 0] = 1e-4

            q = np.quantile(y_slice, t)
            qd[i, :] = np.interp(q, g, dens)

        QD.append(qd)

    return [-np.log(qd + 1e-300) for qd in QD]
