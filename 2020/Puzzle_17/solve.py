import numpy as np
from scipy.ndimage import convolve

kernel = np.ones([3, 3, 3])
kernel[1, 1, 1] = 0


def evolve(cube):
    is_active = cube.copy()
    Ndim = is_active.ndim

    kernel = np.ones([3] * Ndim)
    center = tuple([1] * Ndim)
    kernel[center] = 0

    # Count number of neighbours
    Nneigh = convolve(is_active * 1, kernel, mode="constant", cval=0)
    activate = (is_active & ((Nneigh == 2) | (Nneigh == 3))) | (
        ~is_active & (Nneigh == 3)
    )
    return activate


def parse(lines):
    offset = 6
    size = len(lines.split())
    cube = np.zeros([offset * 2 + size] * 3, dtype=bool)

    for j, line in enumerate(lines.split()):
        for i, c in enumerate(line):
            cube[offset + j, offset + i, offset + size // 2] = c == "#"
    return cube


lines = open("input").read()
cube = parse(lines)
cube0 = cube.copy()

for i in range(6):
    cube = evolve(cube)

print(f"After six iterations, there are {cube.sum()} active cubes.")

# Extend the cube to 4D
extend_dim = np.zeros([1, 1, 1, cube0.shape[0]], dtype=bool)
extend_dim[..., cube0.shape[0] // 2] = 1
cube4 = cube0[:, :, :, None] * extend_dim

for i in range(6):
    cube4 = evolve(cube4)

print(f"After six iterations, there are {cube4.sum()} active hypercubes.")
