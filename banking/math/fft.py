from numpy.fft import fft, ifft, rfft
import matplotlib.pyplot as plt
from pdb import set_trace as st
import numpy as np

def show_fft(x):
	# sampling rate
	sr = len(x)
	# sampling interval
	ts = 1.0/sr
	t = np.arange(0,1,ts)

	X = fft(x)
	N = len(X)
	n = np.arange(N)
	T = N/sr
	freq = n/T 

	plt.figure(figsize = (12, 6))
	plt.subplot(121)

	plt.stem(freq, np.abs(X), 'b', \
	         markerfmt=" ", basefmt="-b")
	plt.xlabel('Freq (Hz)')
	plt.ylabel('FFT Amplitude |X(freq)|')
	plt.xlim(0, 10) # TODO: understand this, 10, 365?

	# HACK
	if (len(t) != len(X)):
		t = np.delete(t, 0)

	plt.subplot(122)
	plt.plot(t, ifft(X), 'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Amplitude')
	plt.tight_layout()
	plt.show()