# Collatz's Big Icecream Problem

## Setup

- `https://www.kaggle.com/datasets/clmentscipion/collatz-sequences-and-metrics-dataset?resource=download`
- `pip install pandas pyarrow` for reading `*.parquet` files


## Theorems and Intuitions

- 2^n are rare but deadly
- n with 3|n never return to an m with 3|m unless 2|n

## Factor returns

Calculate the average change in the number of factors. The intuition here is
that a number is penalized for having many distinct factors because the odd
case returns a number without any of the previous factors (because of the +1).

Further, the following number is never much larger ~3x and so has effectively
the same pool of primes to work from. This suggests a kind of gravity that
guides a number toward a known trajectory and thus to 1.

A surprising number of numbers lose 50% of their value. Which are these?

## Notes:

- Some highly composite odds: 1, 9, 15, 45, 105, 225, 315, 945, and 1575