from fractions import Fraction
from decimal import Decimal
import numpy as np

# first try (no common constraint)

n1 = np.array([0, 1, 2, 3, 4, 5, 6])
y1 = np.array([1, 3, 5, 6, 8, 10, 12])
coeffs1 = np.polyfit(n1, y1, 6)
sol1 = np.polyval(coeffs1, 7)

n2 = np.array([0, 1, 2, 3, 4, 5, 6])
y2 = np.array([1, 3, 4, 6, 8, 9, 10])
coeffs2 = np.polyfit(n2, y2, 6)
sol2 = np.polyval(coeffs2, 7)

sol1 == sol2

# second try

# Original data
n = np.array([0, 1, 2, 3, 4, 5, 6])
y1 = np.array([1, 3, 5, 6, 8, 10, 12])
y2 = np.array([1, 3, 4, 6, 8, 9, 10])

# Vandermonde matrices for degree 6 (seven terms each)
V = np.vander(n, 7)

# Build block diagonal system
A = np.block([
    [V, np.zeros_like(V)],      # equations for first sequence
    [np.zeros_like(V), V]       # equations for second sequence
])

b = np.concatenate([y1, y2])

# Add the constraint at n=7
constraint_row = np.concatenate([
    7 ** np.arange(6, -1, -1),  # a coefficients multiplied by n=7 powers
    -7 ** np.arange(6, -1, -1)  # b coefficients (negative to enforce equality)
])
A = np.vstack([A, constraint_row])
b = np.append(b, 0)             # The constraint equation equates to 0

# Solve for 14 coefficients (a0..a6, b0..b6)
solution = np.linalg.lstsq(A, b, rcond=None)[0]
a_coeffs = solution[:7]
b_coeffs = solution[7:]

# Check values at n=7
val1 = np.polyval(a_coeffs, 7)
val2 = np.polyval(b_coeffs, 7)
print(val1, val2, "float")  # Should be equal

# Rational
poly1 = lambda x: \
    (9/997) * x**6 + \
    (163/-948) * x**5 + \
    (739/601) * x**4 + \
    (691/-172) * x**3 + \
    (2557/448) * x**2 + \
    (645/-871) * x**1 + \
    (489/490)

poly2 = lambda x: \
    (1/288) * x**6 + \
    (32/-789) * x**5 + \
    (46/555) * x**4 + \
    (293/590) * x**3 + \
    (1185/-583) * x**2 + \
    (2060/593) * x**1 + \
    (491/490)

val1 = poly1(7)
val2 = poly2(7)

print(val1, val2, "rational")  # Should be equal
