try:
	from functools import cache
except ImportError:  # Python<3.9
	from functools import lru_cache

	def cache(f):
		return lru_cache(maxsize=None)(f)
