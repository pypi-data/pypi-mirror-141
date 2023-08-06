# GNU GPLv3, see LICENSE

import random
import unittest
from unittest import TestCase

from ..gf256 import _gfmul
from ..gf256 import *


class TestGF256(TestCase):
	def test__gfmul(self):
		self.assertEqual(_gfmul(0, 0), 0)
		self.assertEqual(_gfmul(1, 1), 1)
		self.assertEqual(_gfmul(2, 2), 4)
		self.assertEqual(_gfmul(0, 21), 0)
		self.assertEqual(_gfmul(0x53, 0xca), 0x01)
		self.assertEqual(_gfmul(0xff, 0xff), 0x13)

	def test_gfmul(self):
		for a in range(256):
			for b in range(256):
				self.assertEqual(_gfmul(a, b), gfmul(a, b))

	def test_gfpow(self):
		self.assertEqual(gfpow(0, 0), 1)

		for i in range(1, 256):
			self.assertEqual(gfpow(i, 0), 1)
			self.assertEqual(gfpow(i, 1), i)
			self.assertEqual(gfpow(0, i), 0)
			self.assertEqual(gfpow(1, i), 1)
			self.assertEqual(gfpow(i, 256), i)
			self.assertEqual(gfpow(i, 2), gfmul(i, i))

		random.seed(1918)
		for i in range(256):
			j = random.randint(2, 255)
			k = random.randint(3, 255)
			y = 1
			for m in range(k):
				y = gfmul(y, j)
			self.assertEqual(gfpow(j, k), y)

	def test_evaluate(self):
		for x in range(256):
			(a0, a1, a2, a3) = (x, x>>1, x>>2, x>>3)
			self.assertEqual(evaluate([17], x), 17)  # constant polynomial
			self.assertEqual(evaluate([a3, a2, a1, a0], 0), x)  # any polynomial at 0
			self.assertEqual(evaluate([a3, a2, a1, a0], 1), a0^a1^a2^a3)  # polynomial at 1 == sum of coefficients

	def test_get_constant_coef(self):
		weights = compute_weights((1, 2, 3))
		ys = (1, 2, 3)
		self.assertEqual(get_constant_coef(weights, ys), 0)

		random.seed(17)
		random_matches = 0
		for i in range(10):
			k = random.randint(2, 255)

			# exact
			res = self.check_coefs_match(k, k)
			self.assertEqual(res[0], res[1])

			# overdetermined
			res = self.check_coefs_match(k, 256)
			self.assertEqual(res[0], res[1])

			# underdetermined => random
			res = self.check_coefs_match(k, k-1)
			if res[0]==res[1]:
				random_matches += 1
		self.assertLess(random_matches, 2)  # with a chance (255/256)**10=0.96 there should be no match

	def check_coefs_match(self, k, m):
		coefs = [random.randint(0, 255) for i in range(k)]
		points = [(j, evaluate(coefs, j)) for j in range(1, 256)]
		random.shuffle(points)

		(xs, ys) = zip(*points[:m])
		weights = compute_weights(xs)
		return (get_constant_coef(weights, ys), coefs[-1])


if __name__=='__main__':
	unittest.main()
