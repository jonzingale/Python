# The goal here is to experiment with
# using Kullback-Leibler Divergence
# as a metric on the set of probable primes.
# I am not very positive there is a meaningful
# way to do so, but HEY.

# ary = [p(i) * log(q(i)/p(i)) for i in range(1,infinity)]
# (sum ary) * -1


from scipy.stats import *
from pdb import set_trace as st

E = 10**(-10)

# must have same length
relP = entropy([1, 1, 1, 1, E], [E, 1 , 1, E, 1])

# gives the 
def witnessTo(p):
	testimony = []
	for a in range(1,p):
		if a**p % p == a:
			testimony.append(1/p)
		else:
			testimony.append(E)
	return(testimony)

# gives the witnesses bias
def fromWitness(a):
	testimony = []
	for p in range(2,10**4):
		if a**p % p == a:
			testimony.append(1)
		else:
			testimony.append(E)
	return(testimony)

# normalize the dimension of both arrays
def normalize(a, b):
	if len(a) > len(b):
		while len(a) > len(b):
			b.append(E)
	else:
		while len(a) < len(b):
			a.append(E)
	return(a, b)

# determines distances for a witnesses bias
# to the probable primality of numbers
def klWitnesses(a, b):
	aa = fromWitness(a)
	bb = fromWitness(b)
	aNorm, bNorm = normalize(aa, bb)

	wass = wasserstein_distance(aNorm, bNorm)
	energy = energy_distance(aNorm, bNorm)
	kl = entropy(aNorm, bNorm)
	return([wass, energy, kl])

# determines distances of probable primes
def klPrimes(a, b):
	aa = witnessTo(a)
	bb = witnessTo(b)
	aNorm, bNorm = normalize(aa, bb)

	wass = wasserstein_distance(aNorm, bNorm)
	energy = energy_distance(aNorm, bNorm)
	kl = entropy(aNorm, bNorm)
	return([wass, energy, kl])

print('klPrimes')
print(['wasserstein_distance','energy_distance','kullback-leibler'])
print(klPrimes(3, 167))
print(klPrimes(3, 17))
print(klPrimes(30, 17))

print('\nklWitnesses')
print(['wasserstein_distance','energy_distance','kullback-leibler'])
print(klWitnesses(3, 167))
print(klWitnesses(3, 17))
print(klWitnesses(30, 17))


# st()