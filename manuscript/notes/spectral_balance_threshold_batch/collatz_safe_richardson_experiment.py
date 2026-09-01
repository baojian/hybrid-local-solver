#!/usr/bin/env python3
"""Explore maximal residual-positive Richardson steps on Stieltjes systems.

This is a counterexample search, not theorem evidence.  The iterate uses

    gamma = min_i r_i / (A r)_i  over coordinates with (A r)_i > 0,

so both the solution and residual remain nonnegative for a nonnegative load.
"""

import argparse

import numpy as np


def normalized_page_rank(adjacency, alpha, shift=0.0):
    degree = adjacency.sum(axis=1)
    normalized = adjacency / np.sqrt(degree[:, None] * degree[None, :])
    return (
        (1 + alpha) / 2 * np.eye(len(adjacency))
        - (1 - alpha) / 2 * normalized
        + shift * np.eye(len(adjacency))
    )


def path_graph(n):
    adjacency = np.zeros((n, n))
    for i in range(n - 1):
        adjacency[i, i + 1] = adjacency[i + 1, i] = 1
    return adjacency


def broom_graph(alpha):
    ballast = int(np.ceil(10 / alpha))
    handle = int(np.ceil(3 / np.sqrt(alpha)))
    n = 1 + ballast + handle
    adjacency = np.zeros((n, n))
    for leaf in range(1, ballast + 1):
        adjacency[0, leaf] = adjacency[leaf, 0] = 1
    previous = 0
    for vertex in range(ballast + 1, n):
        adjacency[previous, vertex] = adjacency[vertex, previous] = 1
        previous = vertex
    return adjacency


def safe_collatz(amat, rhs, tolerance=1e-8, max_steps=2_000_000):
    residual = rhs.copy()
    initial = np.linalg.norm(residual)
    steps = 0
    while np.linalg.norm(residual) > tolerance * initial and steps < max_steps:
        image = amat @ residual
        positive = image > 1e-15 * max(1.0, np.linalg.norm(image, np.inf))
        if not np.any(positive):
            raise RuntimeError("no positive Collatz denominator")
        gamma = np.min(residual[positive] / image[positive])
        if gamma <= 0:
            raise RuntimeError("nonpositive safe step")
        residual -= gamma * image
        residual[np.abs(residual) < 5e-14 * initial] = 0
        if np.min(residual) < -2e-11 * initial:
            raise RuntimeError("residual positivity lost")
        residual = np.maximum(residual, 0)
        steps += 1
    return steps, np.linalg.norm(residual) / initial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("path", "broom"), default="path")
    parser.add_argument("--alpha", type=float, default=1e-3)
    parser.add_argument("--shift", type=float, default=0.0)
    parser.add_argument("--tolerance", type=float, default=1e-8)
    args = parser.parse_args()

    if args.family == "path":
        adjacency = path_graph(int(np.ceil(4 / np.sqrt(args.alpha))))
    else:
        adjacency = broom_graph(args.alpha)
    amat = normalized_page_rank(adjacency, args.alpha, args.shift)
    rhs = np.zeros(len(adjacency))
    rhs[0] = 1
    steps, relative = safe_collatz(amat, rhs, args.tolerance)
    print(
        f"family={args.family} n={len(adjacency)} alpha={args.alpha:.3e} "
        f"shift={args.shift:.3e} steps={steps} "
        f"steps_sqrt_floor={steps * np.sqrt(args.alpha + args.shift):.6g} "
        f"relative_residual={relative:.3e}"
    )


if __name__ == "__main__":
    main()
