import re

ELEMENT_RE = re.compile(r"([A-Z][a-z]?)(\d*)")

def parse_formula(formula: str) -> dict[str, int]:
    """
    Parse chemical formulas like:
      Fe2(SO4)3, Ca(OH)2, H2O
    Supports parentheses ().
    Does NOT support charges or hydrates (·).
    """
    formula = formula.replace(" ", "")
    if not formula:
        raise ValueError("Empty formula")

    def parse_section(s: str, i: int = 0) -> tuple[dict[str, int], int]:
        counts: dict[str, int] = {}
        while i < len(s):
            if s[i] == "(":
                inner_counts, i = parse_section(s, i + 1)
                if i >= len(s) or s[i] != ")":
                    raise ValueError(f"Unmatched '(' in {formula}")
                i += 1  # skip ')'

                # multiplier after ')'
                m = ""
                while i < len(s) and s[i].isdigit():
                    m += s[i]
                    i += 1
                mult = int(m) if m else 1

                for el, c in inner_counts.items():
                    counts[el] = counts.get(el, 0) + c * mult

            elif s[i] == ")":
                return counts, i

            else:
                match = ELEMENT_RE.match(s, i)
                if not match:
                    raise ValueError(f"Could not parse near '{s[i:]}' in {formula}")

                el, num = match.groups()
                mult = int(num) if num else 1
                counts[el] = counts.get(el, 0) + mult
                i = match.end()

        return counts, i

    counts, end = parse_section(formula, 0)
    if end != len(formula):
        raise ValueError(f"Could not fully parse {formula}")
    return counts


def parse_equation(eq: str) -> tuple[list[str], list[str]]:
    """
    Returns (reactants, products) as lists.
    Accepts '->' or '=' as arrow.
    """
    eq = eq.strip().replace("=", "->")
    if "->" not in eq:
        raise ValueError("Equation must contain '->' (or '=')")

    left, right = eq.split("->", 1)

    reactants = [x.strip() for x in left.split("+") if x.strip()]
    products = [x.strip() for x in right.split("+") if x.strip()]

    if not reactants or not products:
        raise ValueError("Equation must have reactants and products")

    return reactants, products