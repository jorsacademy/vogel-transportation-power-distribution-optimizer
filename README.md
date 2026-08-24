# Vogel Transportation Power Distribution Optimizer

A small, dependency-free Python implementation of Vogel's Approximation Method (VAM) for a balanced transportation problem, demonstrated with a power-distribution case.

## Problem

Three power plants have capacities of 25, 40, and 30 million kWh. City demands are forecast to rise by 20%, giving:

- City 1: 36 million kWh
- City 2: 42 million kWh
- City 3: 30 million kWh

The plants supply 95 million kWh in total, while demand is 108 million kWh. The 13 million kWh shortfall is purchased from an external grid at a cost of $1,000 per million kWh. The external grid is not allowed to serve City 3.

The transportation costs used in this repository are the assignment's numerical values, expressed in USD as requested:

| Source | City 1 | City 2 | City 3 | Supply |
|---|---:|---:|---:|---:|
| Plant 1 | $600 | $700 | $400 | 25 |
| Plant 2 | $320 | $300 | $350 | 40 |
| Plant 3 | $500 | $480 | $450 | 30 |
| External Grid | $1,000 | $1,000 | Not allowed | 13 |
| Demand | 36 | 42 | 30 | |

## Verified result

For this instance, Vogel's Approximation Method produces:

| Source | City 1 | City 2 | City 3 |
|---|---:|---:|---:|
| Plant 1 | 0 | 0 | 25 |
| Plant 2 | 0 | 40 | 0 |
| Plant 3 | 23 | 2 | 5 |
| External Grid | 13 | 0 | 0 |

Total cost: **$49,710**.

This allocation satisfies every supply constraint, every demand constraint, and the prohibited External Grid -> City 3 route.

An independent linear-programming verification of this specific instance gives the same objective value and allocation, so the VAM solution happens to be optimal for this dataset. VAM itself is a heuristic and does not guarantee an optimal solution for every transportation problem.

## Run

```bash
python main.py
```

## Test

```bash
python -m unittest discover -s tests -v
```

## License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**. Commercial use is not permitted. See `LICENSE` for the full license text.
