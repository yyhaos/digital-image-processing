import numpy as np
from scipy.interpolate import RectBivariateSpline
from skimage.util import img_as_float
from skimage.filters import sobel

def active_contour(image, snake, alpha=0.01, beta=0.1,
    gamma=0.01, max_px_move=1.0,
    max_iterations=2500, convergence=0.1):

    convergence_order = 10

    img = img_as_float(image)
    RGB = img.ndim == 3

    # Find edges using sobel:
    if RGB:
        edge = [sobel(img[:, :, 0]), sobel(img[:, :, 1]),
                sobel(img[:, :, 2])]
    else:
        edge = [sobel(img)]


    # Superimpose intensity and edge images:
    if RGB:
        img = sum(edge)
    else:
        img = edge[0]

    # Interpolate for smoothness:
    intp = RectBivariateSpline(np.arange(img.shape[1]),
                               np.arange(img.shape[0]),
                               img.T, kx=2, ky=2, s=0)

    x, y = snake[:, 0].astype(np.float), snake[:, 1].astype(np.float)
    n = len(x)
    xsave = np.empty((convergence_order, n))  # 随机生成 convergence * n 的矩阵
    ysave = np.empty((convergence_order, n))

    # Build snake shape matrix for Euler equation
    a = np.roll(np.eye(n), -1, axis=0) + \
        np.roll(np.eye(n), -1, axis=1) - \
        2*np.eye(n)  # second order derivative, central difference
    b = np.roll(np.eye(n), -2, axis=0) + \
        np.roll(np.eye(n), -2, axis=1) - \
        4*np.roll(np.eye(n), -1, axis=0) - \
        4*np.roll(np.eye(n), -1, axis=1) + \
        6*np.eye(n)  # fourth order derivative, central difference
    A = -alpha*a + beta*b

    # Only one inversion is needed for implicit spline energy minimization:
    inv = np.linalg.inv(A + gamma*np.eye(n))

    # Explicit time stepping for image energy minimization:
    for i in range(max_iterations):
        fx = intp(x, y, dx=1, grid=False)
        fy = intp(x, y, dy=1, grid=False)

        xn = inv @ (gamma*x + fx)  # x是snake上的点，fx是图像中的点
        yn = inv @ (gamma*y + fy)

        # Movements are capped to max_px_move per iteration:
        dx = max_px_move*np.tanh(xn-x)
        dy = max_px_move*np.tanh(yn-y)

        x += dx
        y += dy

        # Convergence criteria needs to compare to a number of previous
        # configurations since oscillations can occur.
        j = i % (convergence_order+1)
        if j < convergence_order:
            xsave[j, :] = x
            ysave[j, :] = y
        else:
            dist = np.min(np.max(np.abs(xsave-x[None, :]) +
                                 np.abs(ysave-y[None, :]), 1))
            if dist < convergence:
                break

    return np.array([x, y]).T

def circle_points(resolution, center, radius):
    radians = np.linspace(0, 2*np.pi, resolution)
    c = center[0] + radius*np.cos(radians)
    r = center[1] + radius*np.sin(radians)
    return np.array([c, r]).T


