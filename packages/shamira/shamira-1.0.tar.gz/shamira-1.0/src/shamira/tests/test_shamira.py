# GNU GPLv3, see LICENSE
import os
import random
from unittest import TestCase

from .. import *
from .. import gf256
from ..core import encode, decode, detect_encoding, _share_byte, compute_x


class TestShamira(TestCase):
	_urandom = os.urandom

	@classmethod
	def setUpClass(cls):
		random.seed(17)
		os.urandom = lambda n: bytes(random.randint(0, 255) for i in range(n))

	@classmethod
	def tearDownClass(cls):
		os.urandom = cls._urandom

	def test_share_byte(self):
		with self.assertRaises(InvalidParams):  # too few shares
			_share_byte(b"a", 5, 4)
		with self.assertRaises(InvalidParams):  # too many shares
			_share_byte(b"a", 5, 255)
		with self.assertRaises(ValueError):  # not castable to int
			_share_byte("x", 2, 3)

		ys = _share_byte(ord(b"a"), 2, 3)
		xs = compute_x(3)

		weights = gf256.compute_weights(xs)
		self.assertEqual(gf256.get_constant_coef(weights, ys), ord(b"a"))

		weights = gf256.compute_weights(xs[:2])
		self.assertEqual(gf256.get_constant_coef(weights, ys[:2]), ord(b"a"))

		weights = gf256.compute_weights(xs[:1])
		self.assertNotEqual(gf256.get_constant_coef(weights, ys[:1]), ord(b"a"))  # underdetermined => random

	def test_generate_reconstruct_raw(self):
		for (k, n) in [(2, 3), (254, 254)]:
			shares = generate_raw(b"abcd", k, n)
			random.shuffle(shares)
			self.assertEqual(reconstruct_raw(*shares[:k]), b"abcd")
			self.assertNotEqual(reconstruct_raw(*shares[:k-1]), b"abcd")

	def test_generate_reconstruct(self):
		for encoding in ["hex", "b32", "b64"]:
			for secret in [b"abcd", "abcde", "ěščřžý"]:
				for (k, n) in [(2, 3), (254, 254)]:
					raw = isinstance(secret, bytes)
					with self.subTest(enc=encoding, r=raw, sec=secret, k=k, n=n):
						shares = generate(secret, k, n, encoding)
						random.shuffle(shares)
						self.assertEqual(reconstruct(*shares[:k], encoding=encoding, raw=raw), secret)
						self.assertEqual(reconstruct(*shares[:k], raw=raw), secret)
						s = secret if raw else secret.encode("utf-8")
						self.assertNotEqual(reconstruct(*shares[:k-1], encoding=encoding, raw=True), s)
		shares = generate(b"\xfeaa", 2, 3)
		with self.assertRaises(DecodingException):
			reconstruct(*shares)

	def test_encode(self):
		share = (2, b"\x00\x01\x02")
		for (encoding, encoded_str) in [("hex", '000102'), ("b32", 'AAAQE==='), ("b64", 'AAEC')]:
			with self.subTest(enc=encoding):
				self.assertEqual(encode(share, encoding), "2."+encoded_str)

	def test_decode(self):
		with self.assertRaises(MalformedShare):
			decode("AAA")
			decode("1.")
			decode(".AAA")
			decode("1AAA")
			decode("1.0001020f", "hex")
			decode("1.000102030", "hex")
			decode("1.AAAQEAY")
			decode("1.AAAQEAy=")
			decode("1.AAECAw=", "b64")
			decode("1.AAECA?==", "b64")
			decode("256.00010203", "hex")
		self.assertEqual(decode("1.00010203", "hex"), (1, b"\x00\x01\x02\x03"))
		self.assertEqual(decode("2.AAAQEAY=", "b32"), (2, b"\x00\x01\x02\x03"))
		self.assertEqual(decode("3.AAECAw==", "b64"), (3, b"\x00\x01\x02\x03"))

	def testDetectEncoding(self):
		for shares in [
			["1.00010f"],  # bad case
			["1.000102030"],  # bad char count
			["1.AAAQEAY"],  # no padding
			["1.AAAQe==="],  # bad case
			["1.AAECA?=="],  # bad char
			["1.AAECAw="],  # bad padding
			["1.000102", "2.AAAQEAY="],  # mixed encoding
			["1.000102", "2.AAECAw=="],
			["1.AAECAw==", "2.AAAQE==="],
			[".00010203"],  # no index
			["00010203"]  # no index
		]:
			with self.subTest(shares=shares):
				with self.assertRaises(DetectionException):
					detect_encoding(shares)
		self.assertEqual(detect_encoding(["10.00010203"]), "hex")
		self.assertEqual(detect_encoding(["2.AAAQEAY="]), "b32")
		self.assertEqual(detect_encoding(["3.AAECAw=="]), "b64")
		self.assertEqual(detect_encoding(["3.AAECAwQF", "1.00010203"]), "b64")
