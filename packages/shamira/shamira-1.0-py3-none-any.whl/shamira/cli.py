# GNU GPLv3, see LICENSE

import sys
from argparse import ArgumentParser

from .version import __version__
from .core import generate, reconstruct, SException
from .benchmark import build_subparsers as build_benchmark


def run():
	parser = ArgumentParser(prog="Shamira")
	parser.add_argument("-V", "--version", action="version", version='%(prog)s {}'.format(__version__))
	subparsers = parser.add_subparsers()

	build_split_parser(subparsers.add_parser("split"))
	build_join_parser(subparsers.add_parser("join"))
	build_benchmark(subparsers.add_parser("benchmark"))

	parser.set_defaults(func=lambda _: parser.error("missing command"))

	args = parser.parse_args()
	args.func(args)


def build_split_parser(parser):
	parser.add_argument("-k", type=int, required=True, help="number of shares necessary for recovering the secret")
	parser.add_argument("-n", type=int, required=True, help="number of generated shares")

	encoding = parser.add_mutually_exclusive_group()
	encoding.add_argument("--hex", action="store_true", help="encode shares' bytes as a hexadecimal string")
	encoding.add_argument("--b32", action="store_true", help="encode shares' bytes as a base32 string")
	encoding.add_argument("--b64", action="store_true", help="encode shares' bytes as a base64 string")

	parser.add_argument("--label", help="any label to prefix the shares with")
	parser.add_argument("--omit_k_n", action="store_true", help="suppress the default shares prefix")

	parser.add_argument("secret", nargs="?", help="a secret to be split. Can be provided on the command line,"
		" redirected through stdin, or will be asked for interactively.")
	parser.set_defaults(func=_generate)
	

def build_join_parser(parser):
	encoding = parser.add_mutually_exclusive_group()
	encoding.add_argument("--hex", action="store_true", help="decode shares' bytes from a hexadecimal string")
	encoding.add_argument("--b32", action="store_true", help="decode shares' bytes from a base32 string")
	encoding.add_argument("--b64", action="store_true", help="decode shares' bytes from a base64 string")

	parser.add_argument("-r", "--raw", action="store_true", help="return the secret as raw bytes")
	parser.add_argument("share", nargs="*", help="shares to be joined. Can be provided on the command line,"
		" redirected through stdin, or will be asked for interactively.")
	parser.set_defaults(func=_reconstruct)


def _generate(args):
	encoding = get_encoding(args) or "b32"

	if args.secret:  # provided as a positional argument
		secret = args.secret
	elif sys.stdin.isatty():  # input from terminal
		secret = input("Enter your secret:\n")
	else:  # redirected from other source
		secret = sys.stdin.read()

	try:
		shares = generate(secret, args.k, args.n, encoding, label=args.label, omit_k_n=args.omit_k_n)
		for s in shares:
			print(s)
	except SException as e:
		print(e, file=sys.stderr)


def _reconstruct(args):
	encoding = get_encoding(args)

	if args.share:  # provided as a positional argument
		shares = args.share
	elif sys.stdin.isatty():  # input from terminal
		print("Enter the shares, each on separate line, end with an empty line:")
		shares = []
		while not shares or shares[-1]:
			shares.append(input())
		shares.pop()
	else:  # redirected from other source
		shares = sys.stdin.read().split()

	try:
		print(reconstruct(*shares, encoding=encoding, raw=args.raw))
	except SException as e:
		print(e, file=sys.stderr)


def get_encoding(args):
	if args.hex: return "hex"
	elif args.b32: return "b32"
	elif args.b64: return "b64"
	else: return ""
