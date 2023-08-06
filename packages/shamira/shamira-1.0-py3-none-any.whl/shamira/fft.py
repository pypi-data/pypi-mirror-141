# GNU GPLv3, see LICENSE

import math
import cmath
import itertools

from .util import cache
from .gf256 import gfmul, gfpow

# divisors of 255 and their factors in natural numbers
DIVISORS = [3, 5, 15, 17, 51, 85, 255]
FACTORS = {3: [3], 5: [5], 15: [3, 5], 17: [17], 51: [3, 17], 85: [5, 17], 255: [3, 5, 17]}
# values of n-th square roots in GF256
SQUARE_ROOTS = {3: 189, 5: 12, 15: 225, 17: 53, 51: 51, 85: 15, 255: 3}


def ceil_size(n):
	assert n <= DIVISORS[-1]
	for (i, ni) in enumerate(DIVISORS):
		if ni >= n:
			break

	return ni


@cache
def precompute_x(n):
	"""Return a geometric sequence [1, w, w**2, ..., w**(n-1)], where w**n==1.
	This can be done only for certain values of n."""
	assert n in SQUARE_ROOTS, n
	w = SQUARE_ROOTS[n]  # primitive N-th square root of 1
	return list(itertools.accumulate([1]+[w]*(n-1), gfmul))


def complex_dft(p):
	"""Quadratic formula from the definition. The basic case in complex numbers."""
	N = len(p)
	w = cmath.exp(-2*math.pi*1j/N)  # primitive N-th square root of 1
	y = [0]*N
	for k in range(N):
		xk = w**k
		for n in range(N):
			y[k] += p[n] * xk**n
	return y


def dft(p):
	"""Quadratic formula from the definition. In GF256."""
	N = len(p)
	x = precompute_x(N)
	y = [0]*N
	for k in range(N):
		for n in range(N):
			y[k] ^= gfmul(p[n], gfpow(x[k], n))
	return y


def compute_inverse(N1, N2):
	for i in range(N2):
		if N1*i % N2 == 1:
			return i
	raise ValueError("Failed to find an inverse to {0} mod {1}.".format(N1, N2))


def prime_fft(p, divisors, basic_dft=dft):
	"""https://en.wikipedia.org/wiki/Prime-factor_FFT_algorithm"""
	if len(divisors) == 1:
		return basic_dft(p)
	N = len(p)
	N1 = divisors[0]
	N2 = N//N1
	N1_inv = compute_inverse(N1, N2)
	N2_inv = compute_inverse(N2, N1)

	ys = []
	for n1 in range(N1):  # compute rows
		p_ = [p[(n2*N1+n1*N2) % N] for n2 in range(N2)]
		ys.append(prime_fft(p_, divisors[1:], basic_dft))

	for k2 in range(N2):  # compute cols
		p_ = [row[k2] for row in ys]
		y_ = basic_dft(p_)
		for (yi, row) in zip(y_, ys):  # update col
			row[k2] = yi

	# remap and output
	res = [0]*N
	for k1 in range(N1):
		for k2 in range(N2):
			res[(k1*N2*N2_inv+k2*N1*N1_inv) % N] = ys[k1][k2]
	return res


def evaluate(coefs, n):
	ni = ceil_size(n)
	extended_coefs = coefs + [0]*(ni-len(coefs))
	ys = prime_fft(extended_coefs, FACTORS[ni])

	return ys[:n]
