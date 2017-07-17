from pdb import set_trace as st
from numpy.linalg import *
from numpy import *
import cmath

identity = matrix([[1,0],[0,1]])
ii = complex(0,1)

# Pauli Matrices: generating su2
sig1 = 0.5 * matrix([[0,1],[1,0]])
sig2 = 0.5 * matrix([[0,-ii],[ii,0]])
sig3 = 0.5 * matrix([[1,0],[0,-1]])

# Gell-Mann Matrices: generating su3
gm1 = matrix([[0,1,0],[1,0,0],[0,0,0]])
gm2 = matrix([[0,-ii,0],[ii,0,0],[0,0,0]])
gm3 = matrix([[1,0,0],[0,-1,0],[0,0,0]])
gm4 = matrix([[0,0,1],[0,0,0],[1,0,0]])
gm5 = matrix([[0,0,-ii],[0,0,0],[ii,0,0]])
gm6 = matrix([[0,0,0],[0,0,1],[0,1,0]])
gm7 = matrix([[0,0,0],[0,0,-ii],[0,ii,0]])
gm8 = matrix([[1,0,0],[0,1,0],[0,0,-2]]) * 3**-0.5

complexes = [complex(s,t) for (s,t) in [(1,0), (0,1), (1,1)]]

possible_elems = []
for i in complexes:
  for j in complexes:
    mtx = matrix([[i, 0],[0, j]])
    possible_elems.append(mtx)
    mtx = matrix([[0, i],[j, 0]])
    possible_elems.append(mtx)

# the determinant of a unitary matrix
# is a complex number with norm 1
u2 = [] # those with abs.det == 1
for m in filter(lambda m: abs(det(m))==1, possible_elems): u2.append(m)

su2 = [] # det == 1
for matx in u2:
  if det(matx) == 1: su2.append(matx)

# show that each is Unitary,
# ie. conjugate transpose is inverse.
def test1():
  test = []
  for matx in u2:
    if array_equal(matrix.conjugate(matx).T * matx, identity):
      test.append(matx)
  print(len(test) == len(u2))

# test1()