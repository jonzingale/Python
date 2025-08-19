import matplotlib.pyplot as plt
import numpy as np

def collatz(n):
  if n % 2 == 0:
    return(n//2)
  else:
    return(3*n+1)

def iterated_collatz(n):
  accum = []
  while n > 1:
    accum.append(n)
    n = collatz(n)
  accum.append(1)
  return(accum)

def count_factors(n):
    count = 0
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            count += 2 if i != n // i else 1
    return count

def pct_diff(a, b):
    if a == 0:
        return float('inf') # Avoid division by zero
    return (b - a) / a

def collatz_factors_pct_stepwise(n):
    path = iterated_collatz(n)
    print(path)

    factors_list = [count_factors(x) for x in path]
    print(factors_list)

    pct_diffs = []
    for i in range(len(factors_list)-1):
        pct_change = pct_diff(factors_list[i], factors_list[i+1])
        pct_diffs.append(pct_change)

    print(pct_diffs)
    return pct_diffs

def total_returns(ps):
    total = 1.0
    for r in ps:
        total *= (1 + r)
    return total - 1

# random numbers
def random_numbers(n, low, high):
    return np.random.randint(low, high + 1, size=n).tolist()


# Plotting the change in the number of factors
def main(n):
  pct_series = collatz_factors_pct_stepwise(n)
  total_return = total_returns(pct_series)

  plt.figure(figsize=(10, 5))
  plt.plot(range(1, len(pct_series) + 1), pct_series, marker='o')
  plt.title(f'Percent Change in #Factors Along Collatz Path (n={n})')
  plt.xlabel('Collatz Step')
  plt.ylabel('Percent Change in #Factors')
  plt.text(0.5, 0.95, f'Total Return: {total_return:.2%}', ha='center', va='center',
           transform=plt.gca().transAxes, fontsize=12, color='red')
  plt.grid(True)
  plt.tight_layout()
  plt.show()

# main(9999)
for i in random_numbers(20, 99, 9999):
  main(i)