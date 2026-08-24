from src.solver import assert_feasible, example_problem, transportation_cost, vogel_approximation


def main() -> None:
    problem = example_problem()
    allocation = vogel_approximation(problem)
    assert_feasible(problem, allocation)

    labels = ["Plant 1", "Plant 2", "Plant 3", "External Grid"]
    cities = ["City 1", "City 2", "City 3"]

    print("Vogel allocation (million kWh):")
    print(f"{'Source':<15}" + "".join(f"{city:>12}" for city in cities))
    for label, row in zip(labels, allocation):
        print(f"{label:<15}" + "".join(f"{value:>12.0f}" for value in row))

    print(f"\nTotal transportation cost: ${transportation_cost(problem, allocation):,.2f}")


if __name__ == "__main__":
    main()
