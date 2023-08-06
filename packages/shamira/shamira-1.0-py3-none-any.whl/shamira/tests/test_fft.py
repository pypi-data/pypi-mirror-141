# GNU GPLv3, see LICENSE

import random
import functools
import operator
from unittest import TestCase

from .. import gf256
from ..fft import *


def batch_evaluate(coefs, xs):
	return [gf256.evaluate(coefs, x) for x in xs]


class TestFFT(TestCase):
	def test_complex_dft(self):
		self.assertEqual(complex_dft([0]), [0+0j])
		self.assertEqual(complex_dft([1]), [1+0j])
		self.assertEqual(complex_dft([2]), [2+0j])
		all(self.assertAlmostEqual(a, b) for (a, b) in zip(complex_dft([3, 1]), [4+0j, 2+0j]))
		all(self.assertAlmostEqual(a, b) for (a, b) in zip(complex_dft([3, 1, 4]), [8+0j, 0.5+2.59807621j, 0.5-2.59807621j]))
		all(self.assertAlmostEqual(a, b) for (a, b) in zip(complex_dft([3, 1, 4, 1]), [9+0j, -1+0j, 5+0j, -1+0j]))
		all(self.assertAlmostEqual(a, b) for (a, b) in zip(
			complex_dft([3, 1, 4, 1, 5]),
			[14+0j, 0.80901699+2.04087031j, -0.30901699+5.20431056j, -0.30901699-5.20431056j, 0.80901699-2.04087031j]
		))

	def test_complex_prime_fft(self):
		random.seed(1918)
		for divisors in [[3], [2, 3], [3, 5], [3, 5, 17], [2, 3, 5, 7, 11]]:
			n = functools.reduce(operator.mul, divisors)
			coefficients = [random.randint(-128, 127) for i in range(n)]
			a = prime_fft(coefficients, divisors, complex_dft)
			b = complex_dft(coefficients)
			all(self.assertAlmostEqual(ai, bi) for (ai, bi) in zip(a, b))

	def test_finite_dft(self):
		random.seed(1918)
		x = {i: precompute_x(i) for i in [3, 5, 15, 17]}  # all sets of xs

		for n in [3, 5, 15, 17]:
			coefficients = [random.randint(0, 255) for i in range(n)]
			self.assertEqual(
				dft(coefficients),
				batch_evaluate(coefficients[::-1], x[n])
			)

	def test_finite_prime_fft(self):
		random.seed(1918)
		for divisors in [[3], [3, 5], [3, 17], [5, 17], [3, 5, 17]]:
			n = functools.reduce(operator.mul, divisors)
			coefficients = [random.randint(0, 255) for i in range(n)]
			a = prime_fft(coefficients, divisors)
			b = dft(coefficients)
			all(self.assertAlmostEqual(ai, bi) for (ai, bi) in zip(a, b))
