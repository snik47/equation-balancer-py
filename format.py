def format_balanced(coeffs: list[int], reactants: list[str], products: list[str]) -> str:
    left = coeffs[:len(reactants)]
    right = coeffs[len(reactants):]

    def fmt_side(cs: list[int], species: list[str]) -> str:
        parts = []
        for c, sp in zip(cs, species):
            parts.append(sp if c == 1 else f"{c}{sp}")
        return " + ".join(parts)

    return f"{fmt_side(left, reactants)} -> {fmt_side(right, products)}"