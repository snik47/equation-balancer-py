from fractions import Fraction

from balancer.parser import parse_equation, parse_formula
from balancer.linalg import rref, lcm_list, gcd_list

def balance_equation(eq: str) -> tuple[list[int], list[str], list[str]]:
    reactants, products = parse_equation(eq)
    species = reactants + products

    # Parse all species and collect all elements involved
    parsed: list[dict[str, int]] = []
    element_set: set[str] = set()

    for sp in species:
        cnt = parse_formula(sp)
        parsed.append(cnt)
        element_set.update(cnt.keys())

    elements = sorted(element_set)

    # Build conservation matrix: reactants positive, products negative
    m: list[list[Fraction]] = []
    for el in elements:
        row: list[Fraction] = []
        for j, cnt in enumerate(parsed):
            val = cnt.get(el, 0)
            if j >= len(reactants):
                val = -val
            row.append(Fraction(val))
        m.append(row)

    n = len(species)

    # Solve m*x = 0 by setting last coefficient = 1
    A = [row[:-1] for row in m]
    b = [-row[-1] for row in m]
    aug = [A[i] + [b[i]] for i in range(len(A))]

    rref_aug, _ = rref(aug)

    x = [Fraction(0) for _ in range(n)]
    x[-1] = Fraction(1)

    # Extract solution from RREF
    for row in rref_aug:
        pivot_col = None
        for c in range(n - 1):
            if row[c] != 0:
                pivot_col = c
                break

        if pivot_col is None:
            continue

        rhs = row[-1]
        s = Fraction(0)

        for c in range(pivot_col + 1, n - 1):
            if row[c] != 0:
                s += row[c] * x[c]

        x[pivot_col] = (rhs - s) / row[pivot_col]

    # Convert Fractions to smallest integer coefficients
    dens = [f.denominator for f in x]
    L = lcm_list(dens)
    ints = [int(f * L) for f in x]

    # Ensure positive coefficients
    if all(v <= 0 for v in ints):
        ints = [-v for v in ints]
    elif any(v < 0 for v in ints):
        neg = sum(1 for v in ints if v < 0)
        pos = sum(1 for v in ints if v > 0)
        if neg > pos:
            ints = [-v for v in ints]

    # Reduce by gcd
    g = gcd_list([abs(v) for v in ints if v != 0])
    ints = [v // g for v in ints]

    if any(v == 0 for v in ints):
        raise ValueError("Could not balance this equation (zero coefficient).")

    return ints, reactants, products
