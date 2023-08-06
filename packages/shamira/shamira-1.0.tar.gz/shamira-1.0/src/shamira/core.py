# GNU GPLv3, see LICENSE

import os
import re
import base64
import binascii

from . import gf256
from . import fft


class SException(Exception): pass
class InvalidParams(SException): pass
class DetectionException(SException): pass
class DecodingException(SException): pass
class MalformedShare(SException): pass


def compute_x(n):
	return fft.precompute_x(fft.ceil_size(n))[:n]


def _share_byte(secret_b, k, n):
	if not k<=n<255:
		raise InvalidParams("Failed k<=n<255, k={0}, n={1}".format(k, n))
	# we might be concerned with zero coefficients degenerating our polynomial,
	# but there's no reason - we still need k shares to determine it is the case
	coefs = [int(secret_b)]+[int(b) for b in os.urandom(k-1)]
	return fft.evaluate(coefs, n)


def generate_raw(secret, k, n):
	"""Splits secret into shares.

	:param secret: (bytes)
	:param k: number of shares necessary for secret recovery. 1 <= k <= n
	:param n: (int) number of shares generated. 1 <= n < 255
	:return: [(i, (bytes) share), ...]"""
	xs = compute_x(n)
	shares = [_share_byte(b, k, n) for b in secret]
	return [(xi, bytes([s[i] for s in shares])) for (i, xi) in enumerate(xs)]


def reconstruct_raw(*shares):
	"""Tries to recover the secret from its shares.

	:param shares: (((int) i, (bytes) share), ...)
	:return: (bytes) reconstructed secret. Too few shares return garbage."""
	if len({x for (x, _) in shares}) < len(shares):
		raise MalformedShare("Found a non-unique share. Please check your inputs.")

	(xs, payloads) = zip(*shares)
	secret_len = len(payloads[0])
	res = [None]*secret_len
	weights = gf256.compute_weights(xs)
	for i in range(secret_len):
		ys = [s[i] for s in payloads]
		res[i] = (gf256.get_constant_coef(weights, ys))
	return bytes(res)


def generate(secret, k, n, encoding="b32", label="", omit_k_n=False):
	"""Wraps generate_raw().

	:param secret: (str or bytes)
	:param k: number of shares necessary for secret recovery
	:param n: number of shares generated
	:param encoding: {hex, b32, b64} desired output encoding. Hexadecimal, Base32 or Base64.
	:param label: (str) any label to prefix the shares with
	:param omit_k_n: (boolean) suppress the default shares prefix
	:return: [(str) share, ...]"""
	if isinstance(secret,str):
		secret = secret.encode("utf-8")
	shares = generate_raw(secret, k, n)

	prefix = ""
	if label:
		prefix = label + "."
	if not omit_k_n:
		prefix += "{0}.{1}.".format(k, n)

	return [prefix + encode(s, encoding) for s in shares]


def reconstruct(*shares, encoding="", raw=False):
	"""Wraps reconstruct_raw.

	:param shares: ((str) share, ...)
	:param encoding: {hex, b32, b64, ""} encoding of share strings. If not provided or empty, the function tries to guess it.
	:param raw: (bool) whether to return bytes (True) or str (False)
	:return: (str or bytes) reconstructed secret. Too few shares returns garbage."""
	if not encoding:
		encoding = detect_encoding(shares)

	bs = reconstruct_raw(*(decode(s, encoding) for s in shares))
	try:
		return bs if raw else bs.decode(encoding="utf-8")
	except UnicodeDecodeError:
		raise DecodingException('Failed to decode bytes to utf-8. Either you supplied invalid shares, or you missed the "raw" flag. Offending value: {0}'.format(bs))


def encode(share, encoding="b32"):
	if encoding=="hex": f = base64.b16encode
	elif encoding=="b32": f = base64.b32encode
	else: f = base64.b64encode
	(i, bs) = share
	return "{0}.{1}".format(i, f(bs).decode("utf-8"))


def decode(share, encoding="b32"):
	try:
		(*_, i, share_str) = share.split(".")
		i = int(i)
		if not 1<=i<=255:
			raise MalformedShare("Malformed share: Failed 1<=k<=255, k={0}".format(i))
		if encoding=="hex": f = base64.b16decode
		elif encoding=="b32": f = base64.b32decode
		else: f = base64.b64decode
		share_bytes = f(share_str)
		return (i, share_bytes)
	except (ValueError, binascii.Error):
		raise MalformedShare('Malformed share: share="{0}", encoding="{1}"'.format(share, encoding))


def detect_encoding(shares):
	classes = [
		(re.compile(r"(.*\.)?\d+\.([0-9A-F]{2})+"), "hex"),
		(re.compile(r"(.*\.)?\d+\.([A-Z2-7]{8})*([A-Z2-7]{8}|[A-Z2-7]{2}={6}|[A-Z2-7]{4}={4}|[A-Z2-7]{5}={3}|[A-Z2-7]{7}={1})"), "b32"),
		(re.compile(r"(.*\.)?\d+\.([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{2}={2}|[A-Za-z0-9+/]{3}={1})"), "b64")
	]
	for (regexp, res) in classes:
		if all(regexp.fullmatch(share) for share in shares):
			return res
	raise DetectionException("No expected encoding detected")
