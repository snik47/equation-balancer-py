import balancer.solver as solver
from balancer.format import format_balanced

def main():

    print("====================================")
    print("      CHEMICAL EQUATION BALANCER")
    print("====================================")
    print("Example input: C3H8 + O2 -> CO2 + H2O")

    while True:

        eq = input("\nEnter equation (or type 'quit'): ").strip()

        if eq.lower() == "quit":
            print("Goodbye!")
            break

        try:
            coeffs, reactants, products = solver.balance_equation(eq)
            result = format_balanced(coeffs, reactants, products)
            print("Balanced:", result)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()