from numpy.fft import fft, ifft, rfft
import matplotlib.pyplot as plt
from pdb import set_trace as st
import numpy as np

# Investigation:
# How does averaging in to a market change
# with contribution frequency?

# 1. Make and display martingale
# 2. convolve martingale against compound growth

def martingale(x):
	ary = []
	while x > 0:
		p = np.random.rand()
		q = 2 * p - 1
		ary.append(q)
		x -= 1
	return(ary)

def show(ary):
	x = len(ary)
	sr = x
	ts = 1.0/sr
	t = np.arange(0,1,ts)

	n = np.arange(x)
	T = x/sr
	freq = n/T

	plt.figure(figsize = (15, 6), tight_layout=True)
	plt.subplot(111)

	# plt.stem(freq, ary, 'b', markerfmt=" ", basefmt="-b")
	plt.plot(freq, ary, 'g')
	plt.xlabel('Time')
	plt.ylabel('Holdings Value')
	plt.show()

x = 600
m = martingale(x)
f = [np.exp(5*i/x) for i in range(x)]
# f = [i/x for i in range(10)]
# X = np.convolve(m, f)
X = [20*i+j for (i,j) in zip(m, f)]
# show(m) # martingale
show(X) # martingale affected function
