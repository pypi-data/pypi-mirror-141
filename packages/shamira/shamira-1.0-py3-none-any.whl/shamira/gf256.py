# GNU GPLv3, see LICENSE

"""Arithmetic operations on Galois Field 2**8. See https://en.wikipedia.org/wiki/Finite_field_arithmetic"""

from functools import reduce
import operator

from .util import cache


def _gfmul(a, b):
	"""Basic multiplication. Russian peasant algorithm."""
	res = 0
	while a and b:
		if b&1: res ^= a
		if a&0x80: a = 0xff&(a<<1)^0x1b
		else: a <<= 1
		b >>= 1
	return res


g = 3  # generator
E = [None]*256  # exponentials
L = [None]*256  # logarithms
acc = 1
for i in range(256):
	E[i] = acc
	L[acc] = i
	acc = _gfmul(acc, g)
L[1] = 0
INV = [E[255-L[i]] if i!=0 else None for i in range(256)]  # multiplicative inverse


@cache
def gfmul(a, b):
	"""Fast multiplication. Basic multiplication is expensive. a*b==g**(log(a)+log(b))"""
	assert 0<=a<=255, 0<=b<=255
	if a==0 or b==0: return 0
	t = L[a]+L[b]
	if t>255: t -= 255
	return E[t]


@cache
def gfpow(x, k):
	"""Compute x**k."""
	i = 1
	res = 1
	while i <= k:
		if k&i:
			res = gfmul(res, x)
		x = gfmul(x, x)
		i <<= 1

	return res


def evaluate(coefs, x):
	"""Evaluate polynomial's value at x.

	:param coefs: [an, ..., a1, a0]."""
	res = 0

	for a in coefs:  # Horner's rule
		res = gfmul(res, x)
		res ^= a

	return res


def get_constant_coef(weights, y_coords):
	"""Compute constant polynomial coefficient given the points.

	See https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing#Computationally_Efficient_Approach"""
	return reduce(
		operator.xor,
		map(lambda ab: gfmul(*ab), zip(weights, y_coords))
	)


def compute_weights(x_coords):
	assert x_coords

	res = [
			reduce(
				gfmul,
				(gfmul(xj, INV[xj^xi]) for xj in x_coords if xi!=xj),
				1
			) for xi in x_coords
	]

	return res
