import math

def rnd(x,n_sig): return x if (x is None or x==0) else round(x, -int(math.floor(math.log10(abs(x))) - (n_sig - 1)))

def rndAll(obj,n_sig):
	if hasattr(obj,'__iter__'):
		for i,item in enumerate(obj): obj[i] = rndAll(item,n_sig)
	if type(obj)==float: return rnd(obj,n_sig)
	else: return obj
