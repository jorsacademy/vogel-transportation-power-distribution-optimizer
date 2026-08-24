import unittest

from src.solver import assert_feasible, example_problem, transportation_cost, vogel_approximation


class VogelTests(unittest.TestCase):
    def test_assignment_example(self):
        problem = example_problem()
        allocation = vogel_approximation(problem)
        assert_feasible(problem, allocation)

        self.assertEqual(
            allocation,
            [
                [0.0, 0.0, 25.0],
                [0.0, 40.0, 0.0],
                [23.0, 2.0, 5.0],
                [13.0, 0.0, 0.0],
            ],
        )
        self.assertAlmostEqual(transportation_cost(problem, allocation), 49710.0)

    def test_forbidden_external_grid_to_city_3(self):
        problem = example_problem()
        allocation = vogel_approximation(problem)
        self.assertEqual(allocation[3][2], 0.0)


if __name__ == "__main__":
    unittest.main()
