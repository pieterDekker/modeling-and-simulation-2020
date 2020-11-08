import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt


class BoundingCube():
    def __init__(self, center, width) -> None:
        self.center = center
        self.width = width

    def contains(self, point) -> bool:
        # If the absolute difference in all dimensions is less than half the width, the point is within
        return np.all(abs(point - self.center) <= self.width / 2)

    def get_center(self):
        return self.center

    def get_width(self):
        return self.width

    def get_subcubes(self) -> list:
        return [
            BoundingCube(self.center + np.array([x, y, z]), self.width / 2)
            for x in [self.width / 4, -self.width / 4]
            for y in [self.width / 4, -self.width / 4]
            for z in [self.width / 4, -self.width / 4]
        ]

    def get_corners(self) -> list:
        return [
            self.center + np.array([x, y, z])
            for x in [self.width / 2, -self.width / 2]
            for y in [self.width / 2, -self.width / 2]
            for z in [self.width / 2, -self.width / 2]
        ]

    def __str__(self) -> str:
        return f'width: {self.width}\tcenter: {str(self.center)}'


if __name__ == "__main__":
    def plot_bc(bc, ax, c, alph=1):
        for s, e in combinations(bc.get_corners(), 2):
            if np.abs(np.sum(np.abs(s - e)) - bc.width) < 0.005:
                ax.plot3D(*zip(s, e), color=c, alpha=alph)


    fig = plt.figure()
    ax = fig.gca(projection='3d')

    bc = BoundingCube(np.array([0, 0, 0]), 2)
    plot_bc(bc, ax, 'b')
    for subbc in bc.get_subcubes():
        plot_bc(subbc, ax, 'r', 0.5)

    plt.show()
