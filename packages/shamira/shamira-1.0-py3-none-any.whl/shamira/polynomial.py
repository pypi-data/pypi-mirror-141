from itertools import zip_longest

from .gf256 import gfmul,INV


class Polynomial:
	def __init__(self,coefs):
		i,n=0,len(coefs)
		for i in range(n):
			if coefs[n-i-1]!=0: break
		self.coefs=coefs[:n-i]

	def __add__(self, other):
		coefs=[a^b for (a,b) in zip_longest(self.coefs,other.coefs,fillvalue=0)]
		return Polynomial(coefs)

	def __sub__(self, other):
		return self+other

	def __mul__(self, other):
		n=len(self.coefs)+len(other.coefs)-1
		res=[0]*n
		for (i,a) in enumerate(self.coefs):
			for (j,b) in enumerate(other.coefs):
				res[i+j]^=gfmul(a,b)
		return Polynomial(res)

	def __floordiv__(self, k):
		invK=INV[k]
		return Polynomial([gfmul(a,invK) for a in self.coefs])


def getCoefs(*points):
	"""Compute original polynomial coefficients given the points.

	See https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing#Reconstruction"""
	k=len(points)
	res=Polynomial([0])
	for i in range(k):
		li=Polynomial([1])
		(xi,yi)=points[i]
		for j in range(k):
			if i==j: continue
			li*=Polynomial((points[j][0],1)) // (xi^points[j][0])
		res+=Polynomial([yi])*li
	return res.coefs


if __name__=="__main__":
	import random
	import gf256

	k=254
	n=254
	random.seed(19)

	coefs=[random.randrange(1,256) for i in range(k)]
	print(coefs)
	points=[(i,gf256.evaluate(coefs,i)) for i in range(1,n+1)]
	print(points)
	random.shuffle(points)
	print(getCoefs(*points[:k]))
	# print(getCoefs(*points[:k-1]))
