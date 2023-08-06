import cProfile
import timeit

from . import generate, reconstruct
from .tests.test_shamira import TestShamira


def measure(args):
	secret = "1234567890123456"
	shares = generate(secret, args.k, args.n)
	symbols = globals()
	symbols.update(locals())

	time = timeit.timeit("""generate(secret, args.k, args.n)""", number=1, globals=symbols)
	print("The generation took {0:.3}s, {1:.3}s per byte.".format(time, time/16))

	time = timeit.timeit("""reconstruct(*shares)""", number=1, globals=symbols)
	print("The reconstruction took {0:.3}s, {1:.3}s per byte.".format(time, time/16))


def profile(args):
	t = TestShamira()

	cProfile.runctx(r"""t.test_generate_reconstruct()""", globals=globals(), locals=locals(), sort="cumtime")


def build_subparsers(parent):
	parent.set_defaults(func=lambda _: parent.error("missing command"))
	subparsers = parent.add_subparsers()

	profile_parser = subparsers.add_parser("profile")
	profile_parser.set_defaults(func=profile)

	measure_parser = subparsers.add_parser("measure")
	measure_parser.add_argument("-k", type=int, required=True)
	measure_parser.add_argument("-n", type=int, required=True)
	measure_parser.set_defaults(func=measure)
