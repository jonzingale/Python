from sympy import *
x, y, z = symbols('x y z')
init_printing(use_unicode=True)

integrate(exp(-x), (x, 0, oo))

integrate(exp(-x**2 - y**2), (x, -oo, oo), (y, -oo, oo))

sixtyfour = integrate(x*y, (x, 0, 4), (y, 0, 4))

print(sixtyfour)