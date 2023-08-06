import builtins

import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
from matplotlib.patches import Circle


def _get_discs(A, n):

    centers = np.diag(A).astype(complex)
    centers = [(center.real, center.imag) for center in centers]
    radii = np.sum(np.abs(A - np.diag(A) * np.eye(n)), axis=0)

    return centers, radii


def round(center, d):
    return complex(builtins.round(center[0], d), builtins.round(center[1], d))


def gershgorin(A, annotate=False):

    assert A.shape[0] == A.shape[1]
    n = A.shape[0]
    centers, radii = _get_discs(A, n)

    with plt.style.context("seaborn"):
        fig, ax = plt.subplots()

        labels = []

        for center, radius in zip(centers, radii):

            # Plot the circles
            circle = Circle(center, radius, alpha=0.2)
            fig.gca().add_patch(circle)

            # Plot the centers
            ax.scatter(*center, c="k", s=10, marker="x")

            # Get the text coordinates
            center = round(center, 2)
            labels.append(plt.text(center.real, center.imag, center))

        if annotate:
            adjust_text(labels)

        ax.axis("equal")

    return ax
