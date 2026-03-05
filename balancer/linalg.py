from fractions import Fraction
from math import gcd
from functools import reduce

def rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    """
    Reduced Row Echelon Form for a matrix of Fractions.
    Returns (rref_matrix, pivot_cols)
    """
    A = [row[:] for row in matrix]
    rows, cols = len(A), len(A[0])
    r = 0
    pivot_cols: list[int] = []

    for c in range(cols):
        if r >= rows:
            break

        pivot = None
        for rr in range(r, rows):
            if A[rr][c] != 0:
                pivot = rr
                break

        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]

        for rr in range(rows):
            if rr != r and A[rr][c] != 0:
                factor = A[rr][c]
                A[rr] = [A[rr][cc] - factor * A[r][cc] for cc in range(cols)]

        pivot_cols.append(c)
        r += 1

    return A, pivot_cols

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)

def lcm_list(nums: list[int]) -> int:
    return reduce(lcm, nums, 1)

def gcd_list(nums: list[int]) -> int:
    return reduce(gcd, nums)
