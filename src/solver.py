from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class TransportationProblem:
    costs: tuple[tuple[float, ...], ...]
    supply: tuple[float, ...]
    demand: tuple[float, ...]
    forbidden: frozenset[tuple[int, int]] = frozenset()

    def validate(self) -> None:
        if not self.costs or not self.costs[0]:
            raise ValueError("Cost matrix must be non-empty.")
        rows = len(self.costs)
        cols = len(self.costs[0])
        if len(self.supply) != rows or len(self.demand) != cols:
            raise ValueError("Supply/demand dimensions do not match the cost matrix.")
        if any(len(row) != cols for row in self.costs):
            raise ValueError("Cost matrix must be rectangular.")
        if any(value < 0 for value in self.supply + self.demand):
            raise ValueError("Supply and demand must be non-negative.")
        if abs(sum(self.supply) - sum(self.demand)) > 1e-9:
            raise ValueError("Problem must be balanced.")
        for i, j in self.forbidden:
            if not (0 <= i < rows and 0 <= j < cols):
                raise ValueError("Forbidden route is outside the cost matrix.")


def _penalty(values: list[float]) -> float:
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    return values[1] - values[0]


def vogel_approximation(problem: TransportationProblem) -> list[list[float]]:
    """Return a feasible initial solution using Vogel's Approximation Method."""
    problem.validate()
    m, n = len(problem.supply), len(problem.demand)
    remaining_supply = list(problem.supply)
    remaining_demand = list(problem.demand)
    allocation = [[0.0] * n for _ in range(m)]

    while any(x > 1e-9 for x in remaining_supply):
        candidates: list[tuple[float, float, str, int]] = []

        for i in range(m):
            if remaining_supply[i] <= 1e-9:
                continue
            feasible = [
                problem.costs[i][j]
                for j in range(n)
                if remaining_demand[j] > 1e-9 and (i, j) not in problem.forbidden
            ]
            if feasible:
                candidates.append((_penalty(feasible), -min(feasible), "row", i))

        for j in range(n):
            if remaining_demand[j] <= 1e-9:
                continue
            feasible = [
                problem.costs[i][j]
                for i in range(m)
                if remaining_supply[i] > 1e-9 and (i, j) not in problem.forbidden
            ]
            if feasible:
                candidates.append((_penalty(feasible), -min(feasible), "col", j))

        if not candidates:
            raise ValueError("No feasible allocation can satisfy the remaining supply and demand.")

        _, _, kind, index = max(candidates)

        if kind == "row":
            i = index
            feasible_cols = [
                j for j in range(n)
                if remaining_demand[j] > 1e-9 and (i, j) not in problem.forbidden
            ]
            j = min(feasible_cols, key=lambda col: (problem.costs[i][col], col))
        else:
            j = index
            feasible_rows = [
                i for i in range(m)
                if remaining_supply[i] > 1e-9 and (i, j) not in problem.forbidden
            ]
            i = min(feasible_rows, key=lambda row: (problem.costs[row][j], row))

        amount = min(remaining_supply[i], remaining_demand[j])
        allocation[i][j] += amount
        remaining_supply[i] -= amount
        remaining_demand[j] -= amount

    if any(x > 1e-9 for x in remaining_demand):
        raise ValueError("Demand remains unsatisfied.")
    return allocation


def transportation_cost(problem: TransportationProblem, allocation: Sequence[Sequence[float]]) -> float:
    return sum(
        allocation[i][j] * problem.costs[i][j]
        for i in range(len(problem.supply))
        for j in range(len(problem.demand))
    )


def assert_feasible(problem: TransportationProblem, allocation: Sequence[Sequence[float]]) -> None:
    problem.validate()
    m, n = len(problem.supply), len(problem.demand)
    if len(allocation) != m or any(len(row) != n for row in allocation):
        raise AssertionError("Allocation dimensions are invalid.")
    for i in range(m):
        if abs(sum(allocation[i]) - problem.supply[i]) > 1e-9:
            raise AssertionError(f"Supply constraint violated for row {i}.")
    for j in range(n):
        if abs(sum(allocation[i][j] for i in range(m)) - problem.demand[j]) > 1e-9:
            raise AssertionError(f"Demand constraint violated for column {j}.")
    for i, j in problem.forbidden:
        if abs(allocation[i][j]) > 1e-9:
            raise AssertionError(f"Forbidden route ({i}, {j}) was used.")


def example_problem() -> TransportationProblem:
    """Power-distribution example from the assignment, with costs expressed in USD."""
    return TransportationProblem(
        costs=(
            (600.0, 700.0, 400.0),
            (320.0, 300.0, 350.0),
            (500.0, 480.0, 450.0),
            (1000.0, 1000.0, 0.0),
        ),
        supply=(25.0, 40.0, 30.0, 13.0),
        demand=(36.0, 42.0, 30.0),
        forbidden=frozenset({(3, 2)}),
    )
